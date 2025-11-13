#!/usr/bin/env python3
"""
Script to create visual diagrams for the Security Testing API architecture
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io

# Set up matplotlib for better quality
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10

def create_system_architecture_diagram():
    """Create the main system architecture diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Security Testing API - System Architecture', 
            fontsize=20, fontweight='bold', ha='center')
    
    # Client Layer
    client_box = FancyBboxPatch((0.5, 7.5), 2, 1, 
                                boxstyle="round,pad=0.1", 
                                facecolor='#e1f5fe', edgecolor='#0277bd', linewidth=2)
    ax.add_patch(client_box)
    ax.text(1.5, 8, 'Client Apps', fontsize=12, fontweight='bold', ha='center', va='center')
    
    swagger_box = FancyBboxPatch((7.5, 7.5), 2, 1, 
                                 boxstyle="round,pad=0.1", 
                                 facecolor='#e1f5fe', edgecolor='#0277bd', linewidth=2)
    ax.add_patch(swagger_box)
    ax.text(8.5, 8, 'Swagger UI\nDocs', fontsize=12, fontweight='bold', ha='center', va='center')
    
    # FastAPI Application Layer
    fastapi_box = FancyBboxPatch((1, 5.5), 8, 1.5, 
                                 boxstyle="round,pad=0.1", 
                                 facecolor='#f3e5f5', edgecolor='#7b1fa2', linewidth=2)
    ax.add_patch(fastapi_box)
    ax.text(5, 6.7, 'FastAPI Application', fontsize=16, fontweight='bold', ha='center', va='center')
    
    # Auth Router
    auth_router_box = FancyBboxPatch((1.5, 5.8), 3, 0.8, 
                                     boxstyle="round,pad=0.05", 
                                     facecolor='#fff3e0', edgecolor='#f57c00', linewidth=1.5)
    ax.add_patch(auth_router_box)
    ax.text(3, 6.2, 'Authentication Router', fontsize=11, fontweight='bold', ha='center', va='center')
    
    # Security Router
    security_router_box = FancyBboxPatch((5.5, 5.8), 3, 0.8, 
                                         boxstyle="round,pad=0.05", 
                                         facecolor='#fff3e0', edgecolor='#f57c00', linewidth=1.5)
    ax.add_patch(security_router_box)
    ax.text(7, 6.2, 'Security Testing Router', fontsize=11, fontweight='bold', ha='center', va='center')
    
    # Service Layer
    service_layer_box = FancyBboxPatch((1, 3.5), 8, 1.5, 
                                       boxstyle="round,pad=0.1", 
                                       facecolor='#e8f5e8', edgecolor='#388e3c', linewidth=2)
    ax.add_patch(service_layer_box)
    ax.text(5, 4.7, 'Service Layer', fontsize=16, fontweight='bold', ha='center', va='center')
    
    # Auth Service
    auth_service_box = FancyBboxPatch((1.5, 3.8), 3, 0.8, 
                                      boxstyle="round,pad=0.05", 
                                      facecolor='#e3f2fd', edgecolor='#1976d2', linewidth=1.5)
    ax.add_patch(auth_service_box)
    ax.text(3, 4.2, 'Authentication Service', fontsize=11, fontweight='bold', ha='center', va='center')
    
    # Security Service
    security_service_box = FancyBboxPatch((5.5, 3.8), 3, 0.8, 
                                          boxstyle="round,pad=0.05", 
                                          facecolor='#e3f2fd', edgecolor='#1976d2', linewidth=1.5)
    ax.add_patch(security_service_box)
    ax.text(7, 4.2, 'Security Testing Service', fontsize=11, fontweight='bold', ha='center', va='center')
    
    # Data Layer
    data_layer_box = FancyBboxPatch((1, 1.5), 8, 1.5, 
                                    boxstyle="round,pad=0.1", 
                                    facecolor='#fce4ec', edgecolor='#c2185b', linewidth=2)
    ax.add_patch(data_layer_box)
    ax.text(5, 2.7, 'Data Layer', fontsize=16, fontweight='bold', ha='center', va='center')
    
    # JWT Helper
    jwt_box = FancyBboxPatch((1.5, 1.8), 2.5, 0.8, 
                             boxstyle="round,pad=0.05", 
                             facecolor='#f1f8e9', edgecolor='#689f38', linewidth=1.5)
    ax.add_patch(jwt_box)
    ax.text(2.75, 2.2, 'JWT Helper &\nUser Database', fontsize=10, fontweight='bold', ha='center', va='center')
    
    # Security Models
    models_box = FancyBboxPatch((6, 1.8), 2.5, 0.8, 
                                boxstyle="round,pad=0.05", 
                                facecolor='#f1f8e9', edgecolor='#689f38', linewidth=1.5)
    ax.add_patch(models_box)
    ax.text(7.25, 2.2, 'Security Models &\nVulnerability Data', fontsize=10, fontweight='bold', ha='center', va='center')
    
    # Add arrows to show data flow
    # Client to FastAPI
    ax.arrow(1.5, 7.5, 0, -0.8, head_width=0.1, head_length=0.1, fc='black', ec='black')
    ax.arrow(8.5, 7.5, 0, -0.8, head_width=0.1, head_length=0.1, fc='black', ec='black')
    
    # FastAPI to Services
    ax.arrow(3, 5.8, 0, -0.8, head_width=0.1, head_length=0.1, fc='black', ec='black')
    ax.arrow(7, 5.8, 0, -0.8, head_width=0.1, head_length=0.1, fc='black', ec='black')
    
    # Services to Data
    ax.arrow(3, 3.8, 0, -0.8, head_width=0.1, head_length=0.1, fc='black', ec='black')
    ax.arrow(7, 3.8, 0, -0.8, head_width=0.1, head_length=0.1, fc='black', ec='black')
    
    plt.tight_layout()
    plt.savefig('system_architecture.png', bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ System Architecture diagram saved as 'system_architecture.png'")

def create_authentication_flow_diagram():
    """Create authentication flow diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Authentication Flow Diagram', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Components
    components = [
        {'name': 'Client', 'pos': (1, 8), 'color': '#e1f5fe'},
        {'name': 'Auth Router', 'pos': (3.5, 8), 'color': '#fff3e0'},
        {'name': 'Auth Service', 'pos': (6, 8), 'color': '#e8f5e8'},
        {'name': 'JWT Helper', 'pos': (8.5, 8), 'color': '#f1f8e9'}
    ]
    
    for comp in components:
        box = FancyBboxPatch((comp['pos'][0]-0.4, comp['pos'][1]-0.3), 0.8, 0.6, 
                             boxstyle="round,pad=0.05", 
                             facecolor=comp['color'], edgecolor='black', linewidth=1.5)
        ax.add_patch(box)
        ax.text(comp['pos'][0], comp['pos'][1], comp['name'], 
                fontsize=10, fontweight='bold', ha='center', va='center')
    
    # Flow steps
    steps = [
        "1. POST /login",
        "2. authenticate_user()",
        "3. create_tokens()",
        "4. Return JWT tokens",
        "5. GET /me (Bearer token)",
        "6. decode_token()",
        "7. Return user info"
    ]
    
    y_pos = 6.5
    for i, step in enumerate(steps):
        ax.text(0.5, y_pos - i*0.8, step, fontsize=11, ha='left')
        
        # Add arrows for flow
        if i < 3:  # Login flow
            start_x = 1 + i * 2.5
            ax.arrow(start_x, y_pos - i*0.8, 2, 0, head_width=0.1, head_length=0.1, 
                    fc='blue', ec='blue', alpha=0.7)
        elif i == 3:  # Return tokens
            ax.arrow(8.5, y_pos - i*0.8, -7, 0, head_width=0.1, head_length=0.1, 
                    fc='green', ec='green', alpha=0.7)
        elif i > 3:  # User info flow
            start_x = 1 + (i-4) * 2.5
            if i < 6:
                ax.arrow(start_x, y_pos - i*0.8, 2, 0, head_width=0.1, head_length=0.1, 
                        fc='purple', ec='purple', alpha=0.7)
            else:
                ax.arrow(8.5, y_pos - i*0.8, -7, 0, head_width=0.1, head_length=0.1, 
                        fc='orange', ec='orange', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('authentication_flow.png', bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ Authentication Flow diagram saved as 'authentication_flow.png'")

def create_security_testing_flow_diagram():
    """Create security testing flow diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Security Testing Flow Diagram', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Flow steps with positions
    flow_steps = [
        {'text': '1. Client uploads ZIP file', 'pos': (2, 8.5), 'color': '#e3f2fd'},
        {'text': '2. Validate file type', 'pos': (5, 8.5), 'color': '#fff3e0'},
        {'text': '3. Extract ZIP contents', 'pos': (8, 8.5), 'color': '#e8f5e8'},
        {'text': '4. Process each file', 'pos': (2, 7), 'color': '#f1f8e9'},
        {'text': '5. Generate vulnerabilities', 'pos': (5, 7), 'color': '#fce4ec'},
        {'text': '6. Return scan results', 'pos': (8, 7), 'color': '#e0f2f1'},
    ]
    
    for step in flow_steps:
        box = FancyBboxPatch((step['pos'][0]-0.8, step['pos'][1]-0.3), 1.6, 0.6, 
                             boxstyle="round,pad=0.05", 
                             facecolor=step['color'], edgecolor='black', linewidth=1.5)
        ax.add_patch(box)
        ax.text(step['pos'][0], step['pos'][1], step['text'], 
                fontsize=10, fontweight='bold', ha='center', va='center')
    
    # Add arrows
    arrows = [
        ((2.8, 8.5), (4.2, 8.5)),  # 1 to 2
        ((5.8, 8.5), (7.2, 8.5)),  # 2 to 3
        ((8, 8.2), (2, 7.3)),      # 3 to 4 (curved down)
        ((2.8, 7), (4.2, 7)),      # 4 to 5
        ((5.8, 7), (7.2, 7)),      # 5 to 6
    ]
    
    for start, end in arrows:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
    
    # Add vulnerability types
    vuln_types = [
        "Python: SQL injection, XSS",
        "JavaScript: Prototype pollution",
        "JSON: Sensitive data exposure",
        "HTML: Insecure CSP",
        "PHP: Remote file inclusion",
        "Java: XXE vulnerability"
    ]
    
    y_start = 5.5
    ax.text(5, y_start + 0.5, 'Vulnerability Detection by File Type:', 
            fontsize=14, fontweight='bold', ha='center')
    
    for i, vuln in enumerate(vuln_types):
        ax.text(5, y_start - i*0.4, vuln, fontsize=11, ha='center')
    
    plt.tight_layout()
    plt.savefig('security_testing_flow.png', bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ Security Testing Flow diagram saved as 'security_testing_flow.png'")

def create_api_endpoints_diagram():
    """Create API endpoints overview diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'API Endpoints Overview', 
            fontsize=20, fontweight='bold', ha='center')
    
    # Authentication Endpoints
    ax.text(2.5, 8.5, 'Authentication Endpoints', 
            fontsize=16, fontweight='bold', ha='center', color='#1976d2')
    
    auth_endpoints = [
        {'method': 'POST', 'path': '/login', 'desc': 'User authentication'},
        {'method': 'POST', 'path': '/refresh-token', 'desc': 'Token refresh'},
        {'method': 'GET', 'path': '/me', 'desc': 'Get user info'},
    ]
    
    y_pos = 7.8
    for endpoint in auth_endpoints:
        # Method box
        method_color = '#4caf50' if endpoint['method'] == 'GET' else '#ff9800'
        method_box = FancyBboxPatch((0.5, y_pos-0.15), 0.8, 0.3, 
                                    boxstyle="round,pad=0.02", 
                                    facecolor=method_color, edgecolor='black')
        ax.add_patch(method_box)
        ax.text(0.9, y_pos, endpoint['method'], fontsize=10, fontweight='bold', 
                ha='center', va='center', color='white')
        
        # Path and description
        ax.text(1.5, y_pos, endpoint['path'], fontsize=12, fontweight='bold', ha='left', va='center')
        ax.text(3.5, y_pos, endpoint['desc'], fontsize=11, ha='left', va='center')
        y_pos -= 0.6
    
    # Security Testing Endpoints
    ax.text(7.5, 8.5, 'Security Testing Endpoints', 
            fontsize=16, fontweight='bold', ha='center', color='#d32f2f')
    
    security_endpoints = [
        {'method': 'POST', 'path': '/api/v1/security-testing', 'desc': 'Upload & scan ZIP'},
        {'method': 'GET', 'path': '/', 'desc': 'Root endpoint'},
        {'method': 'GET', 'path': '/docs', 'desc': 'API documentation'},
    ]
    
    y_pos = 7.8
    for endpoint in security_endpoints:
        # Method box
        method_color = '#4caf50' if endpoint['method'] == 'GET' else '#ff9800'
        method_box = FancyBboxPatch((5.5, y_pos-0.15), 0.8, 0.3, 
                                    boxstyle="round,pad=0.02", 
                                    facecolor=method_color, edgecolor='black')
        ax.add_patch(method_box)
        ax.text(5.9, y_pos, endpoint['method'], fontsize=10, fontweight='bold', 
                ha='center', va='center', color='white')
        
        # Path and description
        ax.text(6.5, y_pos, endpoint['path'], fontsize=12, fontweight='bold', ha='left', va='center')
        ax.text(8.5, y_pos, endpoint['desc'], fontsize=11, ha='left', va='center')
        y_pos -= 0.6
    
    # Data Models
    ax.text(5, 5, 'Key Data Models', 
            fontsize=16, fontweight='bold', ha='center', color='#7b1fa2')
    
    models = [
        "User, UserLogin, Token",
        "ScanResponse, VulnerabilityItem",
        "ErrorResponse, TokenPayload"
    ]
    
    y_pos = 4.3
    for model in models:
        model_box = FancyBboxPatch((3, y_pos-0.15), 4, 0.3, 
                                   boxstyle="round,pad=0.05", 
                                   facecolor='#f3e5f5', edgecolor='#7b1fa2')
        ax.add_patch(model_box)
        ax.text(5, y_pos, model, fontsize=12, fontweight='bold', ha='center', va='center')
        y_pos -= 0.6
    
    # Security Features
    ax.text(5, 2.5, 'Security Features', 
            fontsize=16, fontweight='bold', ha='center', color='#388e3c')
    
    features = [
        "🔐 JWT Authentication (Access + Refresh tokens)",
        "🛡️ File validation and secure processing",
        "🔍 Mock vulnerability scanning",
        "⚡ CORS middleware and error handling"
    ]
    
    y_pos = 1.8
    for feature in features:
        ax.text(5, y_pos, feature, fontsize=12, ha='center', va='center')
        y_pos -= 0.4
    
    plt.tight_layout()
    plt.savefig('api_endpoints_overview.png', bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ API Endpoints Overview diagram saved as 'api_endpoints_overview.png'")

def create_component_dependency_diagram():
    """Create component dependency diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Component Dependencies', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Components with positions
    components = [
        {'name': 'main.py\n(FastAPI App)', 'pos': (5, 8.5), 'color': '#f3e5f5', 'size': (2, 0.8)},
        {'name': 'auth/routes.py\n(Auth Router)', 'pos': (2.5, 7), 'color': '#fff3e0', 'size': (1.8, 0.6)},
        {'name': 'app/api/v1/security.py\n(Security Router)', 'pos': (7.5, 7), 'color': '#fff3e0', 'size': (1.8, 0.6)},
        {'name': 'auth/service.py\n(Auth Service)', 'pos': (2.5, 5.5), 'color': '#e8f5e8', 'size': (1.8, 0.6)},
        {'name': 'app/services/security_service.py\n(Security Service)', 'pos': (7.5, 5.5), 'color': '#e8f5e8', 'size': (1.8, 0.6)},
        {'name': 'auth/jwt_helper.py\n(JWT Helper)', 'pos': (1, 4), 'color': '#e3f2fd', 'size': (1.6, 0.6)},
        {'name': 'auth/models.py\n(Auth Models)', 'pos': (4, 4), 'color': '#f1f8e9', 'size': (1.6, 0.6)},
        {'name': 'app/models/security.py\n(Security Models)', 'pos': (7, 4), 'color': '#f1f8e9', 'size': (1.6, 0.6)},
        {'name': 'config.py\n(Configuration)', 'pos': (5, 2.5), 'color': '#fce4ec', 'size': (1.6, 0.6)},
    ]
    
    # Draw components
    for comp in components:
        box = FancyBboxPatch((comp['pos'][0] - comp['size'][0]/2, comp['pos'][1] - comp['size'][1]/2), 
                             comp['size'][0], comp['size'][1],
                             boxstyle="round,pad=0.05", 
                             facecolor=comp['color'], edgecolor='black', linewidth=1.5)
        ax.add_patch(box)
        ax.text(comp['pos'][0], comp['pos'][1], comp['name'], 
                fontsize=9, fontweight='bold', ha='center', va='center')
    
    # Dependencies (arrows)
    dependencies = [
        ((5, 8.1), (2.5, 7.4)),    # main -> auth router
        ((5, 8.1), (7.5, 7.4)),    # main -> security router
        ((2.5, 6.6), (2.5, 5.9)),  # auth router -> auth service
        ((7.5, 6.6), (7.5, 5.9)),  # security router -> security service
        ((2.5, 5.1), (1, 4.4)),    # auth service -> jwt helper
        ((2.5, 5.1), (4, 4.4)),    # auth service -> auth models
        ((7.5, 5.1), (7, 4.4)),    # security service -> security models
        ((1, 3.6), (4.2, 2.9)),    # jwt helper -> config
        ((4, 3.6), (4.8, 2.9)),    # auth models -> config
    ]
    
    for start, end in dependencies:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='blue', alpha=0.7))
    
    # Legend
    ax.text(0.5, 1.5, 'Legend:', fontsize=12, fontweight='bold')
    ax.text(0.5, 1.2, '→ Dependency relationship', fontsize=10)
    ax.text(0.5, 0.9, 'Colors represent different layers:', fontsize=10)
    ax.text(0.5, 0.6, '• Purple: Application layer', fontsize=9, color='#7b1fa2')
    ax.text(0.5, 0.3, '• Orange: Router layer', fontsize=9, color='#f57c00')
    ax.text(3, 0.6, '• Green: Service layer', fontsize=9, color='#388e3c')
    ax.text(3, 0.3, '• Blue/Light Green: Data/Helper layer', fontsize=9, color='#1976d2')
    
    plt.tight_layout()
    plt.savefig('component_dependencies.png', bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ Component Dependencies diagram saved as 'component_dependencies.png'")

if __name__ == "__main__":
    print("🎨 Creating visual diagrams for Security Testing API...")
    print()
    
    create_system_architecture_diagram()
    create_authentication_flow_diagram()
    create_security_testing_flow_diagram()
    create_api_endpoints_diagram()
    create_component_dependency_diagram()
    
    print()
    print("🎉 All diagrams created successfully!")
    print("📁 Generated files:")
    print("   • system_architecture.png")
    print("   • authentication_flow.png")
    print("   • security_testing_flow.png")
    print("   • api_endpoints_overview.png")
    print("   • component_dependencies.png")

