from fastapi import APIRouter, HTTPException, Depends
from app.core.auth import authenticate_request as get_current_user
from ...database import supabase

router = APIRouter()

@router.get("/properties")
async def get_properties(current_user: dict = Depends(get_current_user)):
    """
    Get all available properties for a user.
    """
    try:
      # Import database pool
      from app.core.database_pool import DatabasePool
      
      # Initialize pool if needed
      db_pool = DatabasePool()
      await db_pool.initialize()

      async with await db_pool.get_session() as session:
            # Use SQLAlchemy text for raw SQL
            from sqlalchemy import text
            
            query = text("""
                SELECT id, name
                FROM properties 
                WHERE tenant_id = :tenant_id
            """)
            
            result = await session.execute(query, {
                "tenant_id": current_user.tenant_id
            })
        
            return result.mappings().all()
        
    except Exception as e:
        print(f"Error fetching properties: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch properties")