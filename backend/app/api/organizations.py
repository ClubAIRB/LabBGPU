from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io

from app.core.database import get_db
from app.models import Organization, OrganizationType
from app.schemas import OrganizationCreate, OrganizationResponse, OrganizationUpdate

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("/upload", response_model=dict)
async def upload_organizations_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload Excel file with organizations (INN, name, type, region).
    Creates or updates organization records.
    Expected columns: inn, name, type, region
    """
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Файл должен быть в формате Excel")
    
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Validate required columns
        required_columns = ['inn']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(
                status_code=400, 
                detail=f"Файл должен содержать колонки: {', '.join(required_columns)}"
            )
        
        created_count = 0
        updated_count = 0
        
        for _, row in df.iterrows():
            inn = str(row['inn']).strip()
            
            # Validate INN length
            if len(inn) < 10 or len(inn) > 12:
                continue
            
            org_type_str = row.get('type', 'school')
            try:
                org_type = OrganizationType(org_type_str.lower().strip())
            except ValueError:
                org_type = OrganizationType.SCHOOL
            
            organization = db.query(Organization).filter(Organization.inn == inn).first()
            
            if organization:
                # Update existing
                organization.name = row.get('name', organization.name)
                organization.type = org_type
                organization.region = row.get('region', organization.region)
                updated_count += 1
            else:
                # Create new
                organization = Organization(
                    inn=inn,
                    name=row.get('name'),
                    type=org_type,
                    region=row.get('region')
                )
                db.add(organization)
                created_count += 1
        
        db.commit()
        
        return {
            "message": "Организации успешно загружены",
            "created": created_count,
            "updated": updated_count
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке файла: {str(e)}")


@router.get("/", response_model=List[OrganizationResponse])
async def list_organizations(
    skip: int = 0,
    limit: int = 100,
    org_type: OrganizationType | None = None,
    db: Session = Depends(get_db)
):
    """List all organizations with optional filtering."""
    query = db.query(Organization)
    
    if org_type:
        query = query.filter(Organization.type == org_type)
    
    organizations = query.offset(skip).limit(limit).all()
    return organizations


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(org_id: int, db: Session = Depends(get_db)):
    """Get organization by ID."""
    organization = db.query(Organization).filter(Organization.id == org_id).first()
    
    if not organization:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    
    return organization


@router.delete("/{org_id}")
async def delete_organization(org_id: int, db: Session = Depends(get_db)):
    """Delete organization."""
    organization = db.query(Organization).filter(Organization.id == org_id).first()
    
    if not organization:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    
    db.delete(organization)
    db.commit()
    
    return {"message": "Организация удалена"}
