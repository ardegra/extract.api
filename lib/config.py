class Config:
  PRODUCTION = {"DATABASE_ADDRESS": "35.198.212.145:27017"}
  DEVELOPMENT = {"DATABASE_ADDRESS": "35.198.212.145:27017"}
  
  STAGE             = PRODUCTION
  DATABASE_ADDRESS  = STAGE["DATABASE_ADDRESS"]