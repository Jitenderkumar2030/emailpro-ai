from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.db.session import get_db
from app.models.team import Team, TeamMember, TeamInvitation, TeamRole
from app.models.user import User
from app.core.auth import get_current_user
from app.services.email_service import send_team_invitation
import secrets
from datetime import datetime, timedelta

router = APIRouter()

class TeamCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None

class TeamInviteRequest(BaseModel):
    email: EmailStr
    role: str = "member"

@router.post("/create")
def create_team(
    payload: TeamCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    team = Team(
        name=payload.name,
        description=payload.description,
        owner_id=current_user.id
    )
    db.add(team)
    db.flush()
    
    # Add owner as team member
    owner_member = TeamMember(
        team_id=team.id,
        user_id=current_user.id,
        role=TeamRole.OWNER
    )
    db.add(owner_member)
    db.commit()
    
    return {"message": "Team created successfully", "team_id": team.id}

@router.get("/my-teams")
def get_user_teams(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    teams = db.query(Team).join(TeamMember).filter(
        TeamMember.user_id == current_user.id,
        TeamMember.is_active == True
    ).all()
    
    return [{"id": team.id, "name": team.name, "description": team.description} for team in teams]

@router.post("/{team_id}/invite")
def invite_team_member(
    team_id: int,
    payload: TeamInviteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if user has admin rights
    member = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == current_user.id,
        TeamMember.role.in_([TeamRole.OWNER, TeamRole.ADMIN])
    ).first()
    
    if not member:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Create invitation
    token = secrets.token_urlsafe(32)
    invitation = TeamInvitation(
        team_id=team_id,
        email=payload.email,
        role=TeamRole(payload.role),
        token=token,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.add(invitation)
    db.commit()
    
    # Send invitation email
    send_team_invitation(payload.email, token, team_id)
    
    return {"message": "Invitation sent successfully"}
