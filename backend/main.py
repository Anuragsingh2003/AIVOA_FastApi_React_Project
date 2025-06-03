import asyncio
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models import Company, CompanyCreate
from database import get_db_connection, init_pool, close_pool
from contextlib import asynccontextmanager
from typing import List

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pool()
    yield
    await close_pool()

app = FastAPI(title="Company Management API", lifespan=lifespan)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Lifespan handler for startup and shutdown


# Handle OPTIONS requests
@app.options("/companies")
async def options_companies():
    return JSONResponse(status_code=200, content={})

@app.options("/companies/{company_id}")
async def options_company(company_id: int):
    return JSONResponse(status_code=200, content={})

# Create a company
@app.post("/companies", response_model=Company)
async def create_company(company: CompanyCreate):
    conn = None
    try:
        conn = await get_db_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        async with await conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO company (name, location) VALUES (%s, %s)",
                (company.name, company.location)
            )
            await conn.commit()
            company_id = cursor.lastrowid
        return {"id": company_id, **company.dict()}
    except aiomysql.Error as e:
        print(f"MySQL error in create_company: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating company: {str(e)}")
    except Exception as e:
        print(f"Unexpected error in create_company: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating company: {str(e)}")
    finally:
        if conn is not None:
            conn.close()
            print("Connection released in create_company")

# Get all companies
@app.get("/companies", response_model=List[Company])
async def get_companies():
    conn = None
    try:
        conn = await get_db_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        async with await conn.cursor() as cursor:
            await cursor.execute("SELECT id, name, location FROM company")
            rows = await cursor.fetchall()
        return [Company(id=row[0], name=row[1], location=row[2]) for row in rows]
    except aiomysql.Error as e:
        print(f"MySQL error in get_companies: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching companies: {str(e)}")
    except Exception as e:
        print(f"Unexpected error in get_companies: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching companies: {str(e)}")
    finally:
        if conn is not None:
            conn.close()
            print("Connection released in get_companies")

# Get a company by ID
@app.get("/companies/{company_id}", response_model=Company)
async def get_company(company_id: int):
    conn = None
    try:
        conn = await get_db_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        async with await conn.cursor() as cursor:
            await cursor.execute("SELECT id, name, location FROM company WHERE id = %s", (company_id,))
            row = await cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Company not found")
        return Company(id=row[0], name=row[1], location=row[2])
    except aiomysql.Error as e:
        print(f"MySQL error in get_company: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching company: {str(e)}")
    except Exception as e:
        print(f"Unexpected error in get_company: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching company: {str(e)}")
    finally:
        if conn is not None:
            conn.close()
            print("Connection released in get_company")

# Update a company
@app.put("/companies/{company_id}", response_model=Company)
async def update_company(company_id: int, company: CompanyCreate):
    conn = None
    try:
        conn = await get_db_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        async with await conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE company SET name = %s, location = %s WHERE id = %s",
                (company.name, company.location, company_id)
            )
            await conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Company not found")
        return {"id": company_id, **company.dict()}
    except aiomysql.Error as e:
        print(f"MySQL error in update_company: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating company: {str(e)}")
    except Exception as e:
        print(f"Unexpected error in update_company: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating company: {str(e)}")
    finally:
        if conn is not None:
            conn.close()
            print("Connection released in update_company")

# Delete a company
@app.delete("/companies/{company_id}")
async def delete_company(company_id: int):
    conn = None
    try:
        conn = await get_db_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        async with await conn.cursor() as cursor:
            await cursor.execute("DELETE FROM company WHERE id = %s", (company_id,))
            await conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Company not found")
        return {"message": "Company deleted"}
    except aiomysql.Error as e:
        print(f"MySQL error in delete_company: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting company: {str(e)}")
    except Exception as e:
        print(f"Unexpected error in delete_company: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting company: {str(e)}")
    finally:
        if conn is not None:
            conn.close()
            print("Connection released in delete_company")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)