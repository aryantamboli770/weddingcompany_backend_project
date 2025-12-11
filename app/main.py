from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from app.config import settings
from app.utils.database import db_manager
from app.routers import organization, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    print(f"🚀 Starting {settings.APP_NAME}")
    db_manager.connect()
    yield
    # Shutdown
    print(f"🛑 Shutting down {settings.APP_NAME}")
    db_manager.close()


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Multi-tenant Organization Management Service with MongoDB",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(organization.router)
app.include_router(admin.router)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """
    Ultra-premium dark theme Swagger UI
    """
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{settings.APP_NAME} - API Documentation</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
        <link rel="icon" type="image/png" href="https://fastapi.tiangolo.com/img/favicon.png">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            * {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }}
            
            body {{
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
                min-height: 100vh;
            }}
            
            /* Top Bar Styling */
            .swagger-ui .topbar {{
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                padding: 20px 0;
                box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
            }}
            
            .swagger-ui .topbar .download-url-wrapper {{
                display: none;
            }}
            
            /* Main Container */
            .swagger-ui {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 40px 20px;
            }}
            
            /* Info Section */
            .swagger-ui .info {{
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                border-radius: 16px;
                padding: 40px;
                margin: 30px 0;
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }}
            
            .swagger-ui .info .title {{
                color: #fff;
                font-size: 42px;
                font-weight: 700;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 10px;
            }}
            
            .swagger-ui .info .description {{
                color: rgba(255, 255, 255, 0.8);
                font-size: 16px;
                line-height: 1.6;
            }}
            
            /* Scheme Container */
            .swagger-ui .scheme-container {{
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                border-radius: 12px;
                padding: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
            }}
            
            /* Operation Blocks */
            .swagger-ui .opblock {{
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                margin: 20px 0;
                overflow: hidden;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
            }}
            
            .swagger-ui .opblock:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
                border-color: rgba(102, 126, 234, 0.5);
            }}
            
            /* Method Colors - Enhanced Gradients */
            .swagger-ui .opblock.opblock-post {{
                border-left: 4px solid #49cc90;
                background: linear-gradient(90deg, rgba(73, 204, 144, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
            }}
            
            .swagger-ui .opblock.opblock-get {{
                border-left: 4px solid #61affe;
                background: linear-gradient(90deg, rgba(97, 175, 254, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
            }}
            
            .swagger-ui .opblock.opblock-put {{
                border-left: 4px solid #fca130;
                background: linear-gradient(90deg, rgba(252, 161, 48, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
            }}
            
            .swagger-ui .opblock.opblock-delete {{
                border-left: 4px solid #f93e3e;
                background: linear-gradient(90deg, rgba(249, 62, 62, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
            }}
            
            /* Operation Summary */
            .swagger-ui .opblock .opblock-summary {{
                padding: 16px 20px;
                cursor: pointer;
            }}
            
            .swagger-ui .opblock .opblock-summary-path {{
                color: #fff;
                font-weight: 600;
                font-size: 16px;
            }}
            
            .swagger-ui .opblock .opblock-summary-description {{
                color: rgba(255, 255, 255, 0.7);
                font-size: 14px;
            }}
            
            /* Buttons */
            .swagger-ui .btn {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }}
            
            .swagger-ui .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }}
            
            .swagger-ui .btn.execute {{
                background: linear-gradient(135deg, #49cc90 0%, #3ba776 100%);
                box-shadow: 0 4px 12px rgba(73, 204, 144, 0.3);
            }}
            
            .swagger-ui .btn.execute:hover {{
                box-shadow: 0 6px 20px rgba(73, 204, 144, 0.4);
            }}
            
            /* Response Section */
            .swagger-ui .responses-wrapper {{
                background: rgba(0, 0, 0, 0.3);
                border-radius: 8px;
                padding: 20px;
                margin-top: 20px;
            }}
            
            .swagger-ui .response {{
                color: #fff;
            }}
            
            .swagger-ui .response-col_description {{
                color: rgba(255, 255, 255, 0.8);
            }}
            
            /* Tables */
            .swagger-ui table {{
                background: rgba(255, 255, 255, 0.03);
                color: #fff;
                border-radius: 8px;
                overflow: hidden;
            }}
            
            .swagger-ui table thead tr {{
                background: rgba(102, 126, 234, 0.2);
                border-bottom: 2px solid rgba(102, 126, 234, 0.3);
            }}
            
            .swagger-ui table tbody tr {{
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            }}
            
            .swagger-ui table tbody tr:hover {{
                background: rgba(102, 126, 234, 0.1);
            }}
            
            /* Input Fields */
            .swagger-ui input[type=text],
            .swagger-ui input[type=password],
            .swagger-ui input[type=email],
            .swagger-ui textarea,
            .swagger-ui select {{
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: #fff;
                border-radius: 8px;
                padding: 10px;
                transition: all 0.3s ease;
            }}
            
            .swagger-ui input[type=text]:focus,
            .swagger-ui input[type=password]:focus,
            .swagger-ui input[type=email]:focus,
            .swagger-ui textarea:focus,
            .swagger-ui select:focus {{
                outline: none;
                border-color: #667eea;
                background: rgba(102, 126, 234, 0.1);
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
            }}
            
            /* Code Blocks */
            .swagger-ui .highlight-code {{
                background: rgba(0, 0, 0, 0.4);
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .swagger-ui .microlight {{
                color: #a6e22e;
            }}
            
            /* Model Section */
            .swagger-ui .model-box {{
                background: rgba(255, 255, 255, 0.03);
                border-radius: 8px;
                padding: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .swagger-ui .model {{
                color: #fff;
            }}
            
            .swagger-ui .prop-type {{
                color: #fca130;
            }}
            
            .swagger-ui .prop-format {{
                color: rgba(255, 255, 255, 0.6);
            }}
            
            /* Authorization */
            .swagger-ui .auth-wrapper {{
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                border-radius: 12px;
                padding: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .swagger-ui .authorize {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                color: #fff;
                border-radius: 8px;
                padding: 8px 16px;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }}
            
            .swagger-ui .authorize:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }}
            
            /* Scrollbar */
            ::-webkit-scrollbar {{
                width: 12px;
            }}
            
            ::-webkit-scrollbar-track {{
                background: rgba(0, 0, 0, 0.3);
            }}
            
            ::-webkit-scrollbar-thumb {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 6px;
            }}
            
            ::-webkit-scrollbar-thumb:hover {{
                background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            }}
            
            /* Lock Icon for Protected Routes */
            .swagger-ui .authorization__btn.locked {{
                color: #49cc90;
            }}
            
            .swagger-ui .authorization__btn.unlocked {{
                color: rgba(255, 255, 255, 0.5);
            }}
            
            /* Custom Badge Styles */
            .swagger-ui .opblock-tag {{
                color: #fff;
                font-size: 20px;
                font-weight: 600;
                margin: 30px 0 15px 0;
                padding: 12px 20px;
                background: linear-gradient(90deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
                border-left: 4px solid #667eea;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
            window.onload = function() {{
                window.ui = SwaggerUIBundle({{
                    url: '/openapi.json',
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIBundle.SwaggerUIStandalonePreset
                    ],
                    plugins: [
                        SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    layout: "BaseLayout",
                    syntaxHighlight: {{
                        activate: true,
                        theme: "monokai"
                    }},
                    tryItOutEnabled: true,
                    displayRequestDuration: true,
                    filter: true,
                    persistAuthorization: true,
                    defaultModelsExpandDepth: 1,
                    defaultModelExpandDepth: 3,
                    docExpansion: "list",
                }});
            }};
        </script>
    </body>
    </html>
    """)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - Health check
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "database": "connected"
    }