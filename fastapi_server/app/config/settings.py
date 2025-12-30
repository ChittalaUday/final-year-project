"""Configuration for the Career Recommendation API."""
import os
from pathlib import Path
from typing import List, Dict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    app_name: str = "Career Recommendation API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS Configuration
    allowed_origins: List[str] = ["*"]
    
    # Model paths - base_dir should be project root (d:\Projects\Project)
    # __file__ is fastapi_server/app/config/settings.py
    # parent: app/config -> parent: app -> parent: fastapi_server -> parent: Project root
    base_dir: Path = Path(__file__).parent.parent.parent.parent
    models_dir: Path = base_dir / "research" / "Models"
    
    @property
    def model_paths(self) -> Dict:
        """Get model file paths."""
        return {
            "random_forest": self.models_dir / "rf.sav",
            "scaler": self.models_dir / "sc.sav",
            "label_encoder": self.models_dir / "le.pkl",
            "multilabel_binarizer": self.models_dir / "mlb.pkl",
        }
    
    # Course mapping (encoded value -> course name)
    course_mapping: Dict[int, str] = {
        0: "B.A", 1: "B.Arch", 2: "B.Com", 3: "B.Des", 4: "B.Ed",
        5: "B.Plan", 6: "B.E", 7: "B.Pharma", 8: "B.Sc", 9: "B.Tech",
        10: "BA", 11: "BBA", 12: "BCA", 13: "BE", 14: "BHM",
        15: "BMS", 16: "BSc", 17: "BTech", 18: "CA", 19: "Certification course",
        20: "Diploma", 21: "Integrated MTech", 22: "LLB", 23: "M.Arch", 24: "M.Com",
        25: "M.Des", 26: "M.Plan", 27: "M.Sc", 28: "M.Tech", 29: "MA",
        30: "MBA", 31: "MCA", 32: "MCom", 33: "ME", 34: "MS",
        35: "MSc", 36: "MTech", 37: "PGDBA", 38: "PGDM", 39: "PGPM",
        40: "Ph.D",
    }
    
    # Valid interests from the training dataset
    valid_interests: List[str] = [
        "cloud computing", "technology", "understand human behaviour", "sales/marketing",
        "trading", "home interior design", "research", "teaching", "understand human body",
        "content writing", "govt. job", "service", "infrastructure", "financial analysis",
        "take risk for profits", "entrepreneurship", "digital marketing", "market research",
        "agriculture", "construction management", "data analytics", "data scientist",
        "industries", "information technology", "news coverage", "social justice",
        "supply chain analysis", "game industry", "design", "web designing", "web development",
        "social causes", "blockchain", "machine learning", "excel", "sports industry",
        "product life cycle management", "sap consultant in mm", "project management",
        "navy defence related", "oil and gas", "biotechnology", "software developer",
        "hospitality", "salesforce admin", "social media marketing", "software job", "it",
        "urban planning", "data entry or telecalling work", "mobile app development",
        "geography", "geology", "statistical programmer", "software engineering",
        "gardening", "operations", "cyber security", "application development",
        "higher studies", "retailer", "litigation & legal service", "animation",
        "all fields related to data science", "analysis", "architecture and construction",
    ]
    
    # Valid skills from the training dataset
    valid_skills: List[str] = [
        "python", "sql", "java", "critical thinking", "analytic thinking", "programming",
        "work under pressure", "logical skills", "problem solving skills", "people management",
        "communication skills", "accounting skills", "plc allen bradley", "plc ladder logic",
        "labview", "business analysis", "end-to-end project management",
        "cross-functional team leadership", "requirements gathering", "lean six sigma",
        "lean six sigma blackbelt", "productivity improvement", "c", "html", "active listening",
        "gathering information", "artistic/creative skills", "leadership", "editing",
        "writing skills", "medical knowledge", "hr", "teaching", "cost accounting",
        "team work", "tableau", "data visualization skills( power bi/ tableau )",
        "machine learning skills", "artificial intelligence", "matlab", "r", "designing skills",
        "proeficiency in software like staad pro, etabs", "hardware skills", "product knowledge",
        "risk management skills", "cad/cae(autocad/catia/ansys/proe/seimensnx)",
        "finance related skills", "negotiation skills", "mass communication", "sales",
        "interpersonal skills", "wealth management", "financial analysis", "financial modeling",
        "marketing strategy", "financial services", "design and analysis of automobile components",
        "vehicle maintenance and reconditioning", "design for manufacturer and assemble",
        "creativity skills", "excel", "teamwork", "time management", "company secretarial work",
        "legal compliance", "interpersonal communication", "companies act", "indirect taxation",
        "cloud computing", "reporting", "observation skills", "subject knowledge",
        "business knowledge", "market study", "civil & criminal law", "social media marketing",
        "bootstrap", "node.js", "angular", "jira", "trello", "jquery", "javascript", "ajax",
        "php", "codeignitor", "loopback", "hospitality", "polymerase chain reaction (pcr)",
        "life sciences", "protein purification", "protein chemistry", "protein assays",
        "protein electrophoresis", "protein chromatography", "western blotting",
        "protein structure prediction", "protein kinases", "protein characterization",
        "protein engineering", "phytochemistry", "metabolomics", "dna", "biochemistry",
        "bioinformatics", "cell culture", "staad pro", "etabs", "data science", "sap",
        ".net framework", "transact", "technical machine fitter", "c#", "good communication skills",
        "client management", "business analytics", "risk analytics", "sas", "marketing management",
        "market research", "business strategy", "commercial banking", "portfolio management",
        "supply chain management", "business process reengineering", "consumer behaviour",
        "long-term customer relationships", "retail marketing", "financial accounting",
        "credit risk modeling", "security analysis", "working capital management",
        "strategic marketing", "investment banking", "structured finance", "building rapport",
        "2d/3d animation", "oracle", "no"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env file


# Global settings instance
settings = Settings()
