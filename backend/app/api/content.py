from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import pandas as pd
import io
import PyPDF2

from app.core.database import get_db
from app.models.content import NormativeDocument, GeneratedQuestion, CaseTemplate, GeneratedCase
from app.models.settings import PromptTemplate, ModelSettings

router = APIRouter(prefix="/content", tags=["content"])


@router.post("/documents/upload")
async def upload_normative_document(
    title: str = Form(...),
    organization_type: str = Form(...),
    category: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload normative document (PDF or text)."""
    if not file.filename.endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Файл должен быть PDF или TXT")
    
    contents = await file.read()
    content_text = ""
    file_path = f"uploads/{file.filename}"
    
    # Extract text from PDF or read text file
    if file.filename.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(contents))
            for page in pdf_reader.pages:
                content_text += page.extract_text() + "\n"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при чтении PDF: {str(e)}")
    else:
        content_text = contents.decode('utf-8')
    
    document = NormativeDocument(
        title=title,
        organization_type=organization_type,
        category=category,
        file_path=file_path,
        content=content_text
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return {"message": "Документ загружен", "id": document.id}


@router.get("/documents", response_model=List[dict])
async def list_normative_documents(
    organization_type: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all normative documents with optional filtering."""
    query = db.query(NormativeDocument)
    
    if organization_type:
        query = query.filter(NormativeDocument.organization_type == organization_type)
    if category:
        query = query.filter(NormativeDocument.category == category)
    
    documents = query.order_by(NormativeDocument.uploaded_at.desc()).all()
    return [
        {
            "id": d.id,
            "title": d.title,
            "organization_type": d.organization_type,
            "category": d.category,
            "uploaded_at": d.uploaded_at
        }
        for d in documents
    ]


@router.delete("/documents/{doc_id}")
async def delete_normative_document(doc_id: int, db: Session = Depends(get_db)):
    """Delete normative document."""
    document = db.query(NormativeDocument).filter(NormativeDocument.id == doc_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")
    
    db.delete(document)
    db.commit()
    
    return {"message": "Документ удалён"}


@router.post("/questions/generate")
async def generate_questions(
    organization_type: str,
    categories: dict,  # {"кадры": 5, "процессы": 3, ...}
    db: Session = Depends(get_db)
):
    """Generate test questions using AI (placeholder - actual AI integration needed)."""
    # Get prompt template
    template = db.query(PromptTemplate).filter(
        PromptTemplate.category == "test_questions",
        PromptTemplate.organization_type == organization_type
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Шаблон промпта не найден")
    
    generated_count = 0
    
    for category, count in categories.items():
        # Get normative documents for context
        docs = db.query(NormativeDocument).filter(
            NormativeDocument.organization_type == organization_type,
            NormativeDocument.category == category
        ).all()
        
        context = "\n".join([d.content for d in docs if d.content]) if docs else ""
        
        # TODO: Call AI model here with template + context
        # For now, create placeholder questions
        for i in range(count):
            question = GeneratedQuestion(
                category=category,
                question_text=f"Вопрос по категории '{category}' #{i+1} (требуется генерация ИИ)",
                answer_variants=["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4"],
                correct_answer="Вариант 1",
                organization_type=organization_type,
                status="draft"
            )
            db.add(question)
            generated_count += 1
    
    db.commit()
    
    return {"message": f"Сгенерировано {generated_count} вопросов", "count": generated_count}


@router.get("/questions", response_model=List[dict])
async def list_questions(
    category: Optional[str] = None,
    organization_type: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all generated questions with filtering."""
    query = db.query(GeneratedQuestion)
    
    if category:
        query = query.filter(GeneratedQuestion.category == category)
    if organization_type:
        query = query.filter(GeneratedQuestion.organization_type == organization_type)
    if status:
        query = query.filter(GeneratedQuestion.status == status)
    
    questions = query.order_by(GeneratedQuestion.generated_at.desc()).all()
    return [
        {
            "id": q.id,
            "category": q.category,
            "question_text": q.question_text,
            "answer_variants": q.answer_variants,
            "correct_answer": q.correct_answer,
            "status": q.status,
            "organization_type": q.organization_type,
            "generated_at": q.generated_at
        }
        for q in questions
    ]


@router.put("/questions/{question_id}")
async def update_question(
    question_id: int,
    question_text: Optional[str] = None,
    answer_variants: Optional[list] = None,
    correct_answer: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Update a question."""
    question = db.query(GeneratedQuestion).filter(GeneratedQuestion.id == question_id).first()
    
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    
    if question_text:
        question.question_text = question_text
    if answer_variants:
        question.answer_variants = answer_variants
    if correct_answer:
        question.correct_answer = correct_answer
    if status:
        question.status = status
    
    db.commit()
    
    return {"message": "Вопрос обновлён"}


@router.delete("/questions/{question_id}")
async def delete_question(question_id: int, db: Session = Depends(get_db)):
    """Delete a question."""
    question = db.query(GeneratedQuestion).filter(GeneratedQuestion.id == question_id).first()
    
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    
    db.delete(question)
    db.commit()
    
    return {"message": "Вопрос удалён"}


# Case Templates endpoints
@router.post("/case-templates")
async def create_case_template(
    organization_type: str,
    template_text: str,
    title: Optional[str] = None,
    document_ids: Optional[List[int]] = None,
    db: Session = Depends(get_db)
):
    """Create a case template."""
    template = CaseTemplate(
        organization_type=organization_type,
        title=title,
        template_text=template_text
    )
    
    if document_ids:
        docs = db.query(NormativeDocument).filter(NormativeDocument.id.in_(document_ids)).all()
        template.normative_documents = docs
    
    db.add(template)
    db.commit()
    db.refresh(template)
    
    return {"message": "Шаблон кейса создан", "id": template.id}


@router.get("/case-templates", response_model=List[dict])
async def list_case_templates(
    organization_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all case templates."""
    query = db.query(CaseTemplate)
    
    if organization_type:
        query = query.filter(CaseTemplate.organization_type == organization_type)
    
    templates = query.all()
    return [
        {
            "id": t.id,
            "organization_type": t.organization_type,
            "title": t.title,
            "template_text": t.template_text
        }
        for t in templates
    ]


# Generated Cases endpoints
@router.post("/cases/generate")
async def generate_cases(
    organization_type: str,
    count: int = 1,
    db: Session = Depends(get_db)
):
    """Generate cases using AI (placeholder)."""
    # Get case templates
    templates = db.query(CaseTemplate).filter(
        CaseTemplate.organization_type == organization_type
    ).all()
    
    if not templates:
        raise HTTPException(status_code=404, detail="Шаблоны кейсов не найдены")
    
    generated_count = 0
    
    for i in range(count):
        template = templates[i % len(templates)]
        
        # Get related documents
        docs = template.normative_documents
        
        # TODO: Call AI model to generate case based on template and documents
        case = GeneratedCase(
            organization_type=organization_type,
            case_text=f"Кейс для {organization_type} #{i+1} (требуется генерация ИИ)",
            ai_answer="Ответ ИИ будет сгенерирован позже",
            status="draft"
        )
        db.add(case)
        generated_count += 1
    
    db.commit()
    
    return {"message": f"Сгенерировано {generated_count} кейсов", "count": generated_count}


@router.get("/cases", response_model=List[dict])
async def list_cases(
    organization_type: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all generated cases."""
    query = db.query(GeneratedCase)
    
    if organization_type:
        query = query.filter(GeneratedCase.organization_type == organization_type)
    if status:
        query = query.filter(GeneratedCase.status == status)
    
    cases = query.order_by(GeneratedCase.generated_at.desc()).all()
    return [
        {
            "id": c.id,
            "organization_type": c.organization_type,
            "case_text": c.case_text,
            "ai_answer": c.ai_answer,
            "status": c.status,
            "generated_at": c.generated_at
        }
        for c in cases
    ]


@router.put("/cases/{case_id}")
async def update_case(
    case_id: int,
    case_text: Optional[str] = None,
    ai_answer: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Update a case."""
    case = db.query(GeneratedCase).filter(GeneratedCase.id == case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Кейс не найден")
    
    if case_text:
        case.case_text = case_text
    if ai_answer:
        case.ai_answer = ai_answer
    if status:
        case.status = status
    
    db.commit()
    
    return {"message": "Кейс обновлён"}


@router.delete("/cases/{case_id}")
async def delete_case(case_id: int, db: Session = Depends(get_db)):
    """Delete a case."""
    case = db.query(GeneratedCase).filter(GeneratedCase.id == case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Кейс не найден")
    
    db.delete(case)
    db.commit()
    
    return {"message": "Кейс удалён"}
