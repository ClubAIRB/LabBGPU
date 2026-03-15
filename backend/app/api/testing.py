from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from app.core.database import get_db
from app.models import Head, TestSession, Organization
from app.models.analytics import ClusterResult, TestingSchedule
from app.models.content import GeneratedQuestion, GeneratedCase

router = APIRouter(prefix="/testing", tags=["testing"])


@router.get("/session/start")
async def start_test_session(
    db: Session = Depends(get_db),
    head_id: int = None  # TODO: Extract from JWT
):
    """Start a new test session - get random questions and cases."""
    if not head_id:
        raise HTTPException(status_code=400, detail="ID руководителя не указан")
    
    head = db.query(Head).filter(Head.id == head_id).first()
    if not head:
        raise HTTPException(status_code=404, detail="Руководитель не найден")
    
    org_type = head.organization.type if head.organization else "school"
    
    # Get published questions (5 per category)
    categories = ["кадры", "процессы", "результаты", "информация", "ресурсы"]
    questions = []
    
    for category in categories:
        cat_questions = db.query(GeneratedQuestion).filter(
            GeneratedQuestion.category == category,
            GeneratedQuestion.organization_type == org_type,
            GeneratedQuestion.status == "published"
        ).limit(5).all()
        
        for q in cat_questions:
            questions.append({
                "id": q.id,
                "category": q.category,
                "question_text": q.question_text,
                "answer_variants": q.answer_variants
            })
    
    # Get published cases (1-2)
    cases = db.query(GeneratedCase).filter(
        GeneratedCase.organization_type == org_type,
        GeneratedCase.status == "published"
    ).limit(2).all()
    
    cases_data = [
        {
            "id": c.id,
            "case_text": c.case_text
        }
        for c in cases
    ]
    
    return {
        "questions": questions,
        "cases": cases_data
    }


@router.post("/session/submit")
async def submit_test_session(
    answers: Dict[str, Any],
    case_answers: Optional[Dict[str, str]] = None,
    db: Session = Depends(get_db),
    head_id: int = None
):
    """Submit test session with answers."""
    if not head_id:
        raise HTTPException(status_code=400, detail="ID руководителя не указан")
    
    head = db.query(Head).filter(Head.id == head_id).first()
    if not head:
        raise HTTPException(status_code=404, detail="Руководитель не найден")
    
    # Calculate scores by category
    scores = {}
    categories = {}
    
    for q_id, answer in answers.items():
        question = db.query(GeneratedQuestion).filter(GeneratedQuestion.id == int(q_id)).first()
        if question:
            if question.category not in categories:
                categories[question.category] = {"total": 0, "correct": 0}
            
            categories[question.category]["total"] += 1
            
            if answer == question.correct_answer:
                categories[question.category]["correct"] += 1
    
    # Calculate percentage scores
    for category, data in categories.items():
        if data["total"] > 0:
            scores[category] = round(data["correct"] / data["total"] * 100)
    
    # Create test session
    session = TestSession(
        head_id=head_id,
        organization_id=head.organization_id,
        answers=answers,
        scores=scores,
        case_answers=case_answers
    )
    
    db.add(session)
    
    # Update head's last test date and results
    head.last_test_date = datetime.utcnow()
    head.last_results = scores
    
    db.commit()
    db.refresh(session)
    
    return {
        "message": "Тестирование завершено",
        "session_id": session.id,
        "scores": scores
    }


@router.get("/session/{session_id}/pdf")
async def generate_test_pdf(
    session_id: int,
    db: Session = Depends(get_db)
):
    """Generate PDF report for test session."""
    session = db.query(TestSession).filter(TestSession.id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    
    head = session.head
    org = session.organization
    
    # Create PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center
    )
    
    content = []
    
    # Title
    content.append(Paragraph("Отчёт о тестировании руководителя", title_style))
    content.append(Spacer(1, 20))
    
    # Info table
    info_data = [
        ["ФИО:", head.full_name or "Не указано"],
        ["Организация:", org.name if org else "Не указано"],
        ["ИНН:", org.inn if org else "Не указано"],
        ["Дата тестирования:", session.test_date.strftime("%d.%m.%Y %H:%M")]
    ]
    
    info_table = Table(info_data, colWidths=[150, 300])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    content.append(info_table)
    content.append(Spacer(1, 30))
    
    # Scores
    content.append(Paragraph("Результаты по категориям:", styles['Heading2']))
    content.append(Spacer(1, 10))
    
    if session.scores:
        scores_data = [["Категория", "Баллы (%)"]]
        for category, score in session.scores.items():
            scores_data.append([category, str(score)])
        
        scores_table = Table(scores_data, colWidths=[250, 100])
        scores_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        content.append(scores_table)
    else:
        content.append(Paragraph("Результаты отсутствуют", styles['Normal']))
    
    content.append(Spacer(1, 30))
    
    # Case answers
    if session.case_answers:
        content.append(Paragraph("Ответы на кейсы:", styles['Heading2']))
        content.append(Spacer(1, 10))
        
        for case_id, answer in session.case_answers.items():
            content.append(Paragraph(f"Кейс #{case_id}:", styles['Heading3']))
            content.append(Paragraph(answer[:500] + ("..." if len(answer) > 500 else ""), styles['Normal']))
            content.append(Spacer(1, 15))
    
    doc.build(content)
    buffer.seek(0)
    
    return {
        "filename": f"report_{session_id}.pdf",
        "content_type": "application/pdf"
    }


# Analytics endpoints
@router.get("/analytics/summary")
async def get_analytics_summary(db: Session = Depends(get_db)):
    """Get overall analytics summary."""
    total_heads = db.query(Head).count()
    total_sessions = db.query(TestSession).count()
    
    # Average scores by category
    sessions = db.query(TestSession).filter(TestSession.scores != None).all()
    
    category_scores = {}
    for session in sessions:
        if session.scores:
            for category, score in session.scores.items():
                if category not in category_scores:
                    category_scores[category] = []
                category_scores[category].append(score)
    
    avg_scores = {
        cat: round(sum(scores) / len(scores)) if scores else 0
        for cat, scores in category_scores.items()
    }
    
    # Sessions by organization type
    org_type_counts = db.query(
        Organization.type, 
        db.func.count(TestSession.id)
    ).join(
        TestSession, Organization.id == TestSession.organization_id
    ).group_by(Organization.type).all()
    
    return {
        "total_heads": total_heads,
        "total_sessions": total_sessions,
        "avg_scores": avg_scores,
        "sessions_by_org_type": dict(org_type_counts)
    }


@router.post("/analytics/cluster")
async def run_clustering(db: Session = Depends(get_db)):
    """Run clustering algorithm on heads (placeholder)."""
    # Get all sessions with scores
    sessions = db.query(TestSession).filter(TestSession.scores != None).all()
    
    if len(sessions) < 3:
        raise HTTPException(status_code=400, detail="Недостаточно данных для кластеризации")
    
    # TODO: Implement actual K-means clustering
    # For now, create a simple placeholder cluster
    
    cluster = ClusterResult(
        cluster_name="Кластер 1",
        description="Автоматически сгенерированный кластер",
        heads_data=[{"head_id": s.head_id, "scores": s.scores} for s in sessions[:10]],
        avg_scores={"кадры": 75, "процессы": 68}
    )
    
    db.add(cluster)
    db.commit()
    
    return {"message": "Кластеризация выполнена", "cluster_id": cluster.id}


@router.get("/analytics/clusters", response_model=List[dict])
async def list_clusters(db: Session = Depends(get_db)):
    """List all cluster results."""
    clusters = db.query(ClusterResult).order_by(ClusterResult.created_at.desc()).all()
    
    return [
        {
            "id": c.id,
            "cluster_name": c.cluster_name,
            "description": c.description,
            "heads_count": len(c.heads_data) if c.heads_data else 0,
            "avg_scores": c.avg_scores,
            "created_at": c.created_at
        }
        for c in clusters
    ]


@router.put("/analytics/clusters/{cluster_id}")
async def update_cluster(
    cluster_id: int,
    cluster_name: Optional[str] = None,
    description: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Update cluster name and description."""
    cluster = db.query(ClusterResult).filter(ClusterResult.id == cluster_id).first()
    
    if not cluster:
        raise HTTPException(status_code=404, detail="Кластер не найден")
    
    if cluster_name:
        cluster.cluster_name = cluster_name
    if description:
        cluster.description = description
    
    db.commit()
    
    return {"message": "Кластер обновлён"}


# Education program generation
@router.post("/analytics/clusters/{cluster_id}/program")
async def generate_education_program(
    cluster_id: int,
    db: Session = Depends(get_db)
):
    """Generate education program for a cluster (placeholder)."""
    cluster = db.query(ClusterResult).filter(ClusterResult.id == cluster_id).first()
    
    if not cluster:
        raise HTTPException(status_code=404, detail="Кластер не найден")
    
    # TODO: Use AI to generate program based on cluster avg_scores
    program_text = f"""
    Образовательная программа для кластера "{cluster.cluster_name}"
    
    На основе анализа результатов тестирования выявлены следующие зоны роста:
    - Средние баллы по категориям: {cluster.avg_scores}
    
    Рекомендации:
    1. Пройти курсы повышения квалификации по слабым категориям
    2. Изучить лучшие практики управления
    3. Участвовать в профессиональных сообществах
    """
    
    return {
        "cluster_id": cluster_id,
        "program_text": program_text
    }


# Schedule endpoints
@router.get("/schedule")
async def list_schedule(
    db: Session = Depends(get_db)
):
    """List all scheduled tests."""
    schedules = db.query(TestingSchedule).order_by(TestingSchedule.test_date).all()
    
    return [
        {
            "id": s.id,
            "organization_inn": s.organization_inn,
            "candidate_name": s.candidate_name,
            "test_date": s.test_date.isoformat(),
            "test_time": s.test_time.isoformat() if s.test_time else None,
            "status": s.status,
            "notes": s.notes
        }
        for s in schedules
    ]


@router.post("/schedule")
async def create_schedule(
    organization_inn: Optional[str] = None,
    candidate_name: Optional[str] = None,
    test_date: str = None,
    test_time: Optional[str] = None,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Create a new test schedule."""
    from datetime import date, time
    
    schedule = TestingSchedule(
        organization_inn=organization_inn,
        candidate_name=candidate_name,
        test_date=date.fromisoformat(test_date),
        test_time=time.fromisoformat(test_time) if test_time else None,
        notes=notes
    )
    
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    
    return {"message": "Тестирование запланировано", "id": schedule.id}


@router.delete("/schedule/{schedule_id}")
async def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """Delete a scheduled test."""
    schedule = db.query(TestingSchedule).filter(TestingSchedule.id == schedule_id).first()
    
    if not schedule:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    
    db.delete(schedule)
    db.commit()
    
    return {"message": "Запись удалена"}
