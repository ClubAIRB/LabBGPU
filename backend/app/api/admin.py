from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.admin import AdminUser
from app.models.settings import PromptTemplate, ModelSettings, EmbeddingModel, SimilarityThreshold
from app.schemas import AdminLoginRequest, AdminLoginResponse
from app.core.security import verify_password, get_password_hash, create_access_token

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/login", response_model=AdminLoginResponse)
async def admin_login(
    request: AdminLoginRequest,
    db: Session = Depends(get_db)
):
    """Admin login endpoint."""
    admin = db.query(AdminUser).filter(AdminUser.username == request.username).first()
    
    if not admin or not verify_password(request.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )
    
    access_token = create_access_token(
        data={"sub": str(admin.id), "type": "admin"},
        expires_delta=None
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Prompt Templates endpoints
@router.get("/prompts", response_model=List[dict])
async def list_prompt_templates(
    category: Optional[str] = None,
    organization_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all prompt templates with optional filtering."""
    query = db.query(PromptTemplate)
    
    if category:
        query = query.filter(PromptTemplate.category == category)
    if organization_type:
        query = query.filter(PromptTemplate.organization_type == organization_type)
    
    templates = query.all()
    return [
        {
            "id": t.id,
            "category": t.category,
            "organization_type": t.organization_type,
            "template_text": t.template_text,
            "updated_at": t.updated_at
        }
        for t in templates
    ]


@router.post("/prompts")
async def create_prompt_template(
    category: str,
    template_text: str,
    organization_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Create a new prompt template."""
    template = PromptTemplate(
        category=category,
        organization_type=organization_type,
        template_text=template_text
    )
    db.add(template)
    db.commit()
    db.refresh(template)
    
    return {"message": "Шаблон промпта создан", "id": template.id}


@router.put("/prompts/{template_id}")
async def update_prompt_template(
    template_id: int,
    template_text: str,
    db: Session = Depends(get_db)
):
    """Update prompt template."""
    template = db.query(PromptTemplate).filter(PromptTemplate.id == template_id).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Шаблон не найден")
    
    template.template_text = template_text
    template.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Шаблон обновлён"}


@router.delete("/prompts/{template_id}")
async def delete_prompt_template(
    template_id: int,
    db: Session = Depends(get_db)
):
    """Delete prompt template."""
    template = db.query(PromptTemplate).filter(PromptTemplate.id == template_id).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Шаблон не найден")
    
    db.delete(template)
    db.commit()
    
    return {"message": "Шаблон удалён"}


# Model Settings endpoints
@router.get("/models", response_model=List[dict])
async def list_model_settings(db: Session = Depends(get_db)):
    """List all AI model settings."""
    models = db.query(ModelSettings).all()
    return [
        {
            "id": m.id,
            "model_name": m.model_name,
            "parameters": m.parameters,
            "is_active": m.is_active,
            "created_at": m.created_at
        }
        for m in models
    ]


@router.post("/models")
async def create_model_setting(
    model_name: str,
    parameters: dict,
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    """Create new model settings."""
    model = ModelSettings(
        model_name=model_name,
        parameters=parameters,
        is_active=is_active
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    
    return {"message": "Настройки модели созданы", "id": model.id}


@router.put("/models/{model_id}")
async def update_model_setting(
    model_id: int,
    parameters: Optional[dict] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Update model settings."""
    model = db.query(ModelSettings).filter(ModelSettings.id == model_id).first()
    
    if not model:
        raise HTTPException(status_code=404, detail="Модель не найдена")
    
    if parameters is not None:
        model.parameters = parameters
    if is_active is not None:
        model.is_active = is_active
    
    db.commit()
    
    return {"message": "Настройки обновлены"}


# Embedding Models endpoints
@router.get("/embeddings", response_model=List[dict])
async def list_embedding_models(db: Session = Depends(get_db)):
    """List all embedding models."""
    models = db.query(EmbeddingModel).all()
    return [
        {
            "id": m.id,
            "model_name": m.model_name,
            "model_type": m.model_type,
            "is_active": m.is_active
        }
        for m in models
    ]


@router.post("/embeddings")
async def create_embedding_model(
    model_name: str,
    model_type: Optional[str] = None,
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    """Create new embedding model."""
    model = EmbeddingModel(
        model_name=model_name,
        model_type=model_type,
        is_active=is_active
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    
    return {"message": "Модель эмбеддингов создана", "id": model.id}


# Similarity Threshold endpoints
@router.get("/threshold", response_model=dict)
async def get_similarity_threshold(db: Session = Depends(get_db)):
    """Get current similarity threshold."""
    threshold = db.query(SimilarityThreshold).first()
    
    if not threshold:
        threshold = SimilarityThreshold(threshold=0.8)
        db.add(threshold)
        db.commit()
        db.refresh(threshold)
    
    return {
        "id": threshold.id,
        "threshold": threshold.threshold,
        "description": threshold.description
    }


@router.put("/threshold")
async def update_similarity_threshold(
    threshold_value: float,
    description: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Update similarity threshold."""
    threshold = db.query(SimilarityThreshold).first()
    
    if not threshold:
        threshold = SimilarityThreshold(
            threshold=threshold_value,
            description=description
        )
        db.add(threshold)
    else:
        threshold.threshold = threshold_value
        if description:
            threshold.description = description
    
    db.commit()
    
    return {"message": "Порог обновлён"}
