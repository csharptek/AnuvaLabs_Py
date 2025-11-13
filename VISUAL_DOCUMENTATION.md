# Security Testing API - Visual Documentation

This document contains visual diagrams and a PowerPoint presentation for the Security Testing API architecture.

## 📊 Visual Diagrams

### 1. System Architecture Overview
![System Architecture](https://github.com/csharptek/AnuvaLabs_Py/blob/codegen-artifacts-store/docs/images/system_architecture.png?raw=true)

This diagram shows the complete system architecture with all layers:
- **Client Layer**: Client applications and Swagger UI documentation
- **API Layer**: FastAPI application with authentication and security routers
- **Service Layer**: Business logic for authentication and security testing
- **Data Layer**: Models, JWT helpers, and mock database

### 2. Authentication Flow
![Authentication Flow](https://github.com/csharptek/AnuvaLabs_Py/blob/codegen-artifacts-store/docs/images/authentication_flow.png?raw=true)

This diagram illustrates the complete authentication process:
1. User login with credentials
2. Token creation and validation
3. Protected endpoint access
4. Token refresh mechanism

### 3. Security Testing Flow
![Security Testing Flow](https://github.com/csharptek/AnuvaLabs_Py/blob/codegen-artifacts-store/docs/images/security_testing_flow.png?raw=true)

This diagram shows the security testing process:
1. ZIP file upload and validation
2. File extraction and processing
3. Vulnerability detection by file type
4. Report generation and cleanup

### 4. API Endpoints Overview
![API Endpoints Overview](https://github.com/csharptek/AnuvaLabs_Py/blob/codegen-artifacts-store/docs/images/api_endpoints_overview.png?raw=true)

This diagram provides a comprehensive view of:
- Authentication endpoints (login, refresh, user info)
- Security testing endpoints (upload, scan, docs)
- Data models and security features
- HTTP methods and response formats

### 5. Component Dependencies
![Component Dependencies](https://github.com/csharptek/AnuvaLabs_Py/blob/codegen-artifacts-store/docs/images/component_dependencies.png?raw=true)

This diagram maps the relationships between different components:
- FastAPI application structure
- Router to service dependencies
- Service to helper/model dependencies
- Configuration and utility connections

## 📋 PowerPoint Presentation

### Download Presentation
**[Security Testing API Architecture.pptx](https://github.com/csharptek/AnuvaLabs_Py/blob/codegen-artifacts-store/docs/Security_Testing_API_Architecture.pptx?raw=true)**

### Presentation Contents (13 Slides)

1. **Title Slide** - Project introduction and overview
2. **Project Overview** - Key features and capabilities
3. **System Architecture** - Visual layer representation
4. **API Endpoints** - Complete endpoint documentation
5. **Authentication Flow** - Step-by-step authentication process
6. **Security Testing Flow** - File processing and scanning workflow
7. **Data Models** - Pydantic models and relationships
8. **Component Dependencies** - Module interactions and dependencies
9. **Security Features** - Current implementation and recommendations
10. **Project File Structure** - Directory organization
11. **Usage Examples** - API request/response samples
12. **Development Setup** - Installation and running instructions
13. **Future Enhancements** - Roadmap and improvements

## 🎯 Key Visual Elements

### Color Coding
- **Blue tones** (`#e1f5fe`, `#e3f2fd`): Client and data components
- **Purple tones** (`#f3e5f5`): FastAPI application layer
- **Orange tones** (`#fff3e0`): Router components
- **Green tones** (`#e8f5e8`): Service layer components
- **Pink tones** (`#fce4ec`): Data and model components
- **Light green** (`#f1f8e9`): Helper and utility components

### Diagram Features
- **Clear component separation** with distinct colors and borders
- **Directional arrows** showing data flow and dependencies
- **Hierarchical layout** representing system layers
- **Consistent styling** across all diagrams
- **High resolution** (300 DPI) for professional presentation

## 📱 Usage Instructions

### Viewing Images
- Click on any image to view full size
- Images are hosted on GitHub with direct access URLs
- All images are in PNG format with transparent backgrounds where appropriate

### Using the PowerPoint
- Download the PPTX file using the link above
- Compatible with Microsoft PowerPoint, Google Slides, and LibreOffice Impress
- Each slide contains detailed information about different aspects of the system
- Use for presentations, documentation, or training purposes

### Integration with Documentation
- These visual elements complement the text-based documentation in `ARCHITECTURE.md`
- Mermaid diagrams in `API_FLOW_DIAGRAMS.md` provide interactive alternatives
- Use together for comprehensive system understanding

## 🔧 Technical Details

### Image Specifications
- **Format**: PNG with high compression
- **Resolution**: 300 DPI for print quality
- **Dimensions**: Optimized for both screen and print viewing
- **Color Space**: RGB for digital display

### PowerPoint Specifications
- **Format**: Microsoft PowerPoint (.pptx)
- **Compatibility**: PowerPoint 2016+ / Google Slides / LibreOffice
- **Slide Size**: Standard 16:9 widescreen format
- **Fonts**: Standard system fonts for maximum compatibility

## 📚 Related Documentation

- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Comprehensive text-based architecture documentation
- **[API_FLOW_DIAGRAMS.md](./API_FLOW_DIAGRAMS.md)** - Interactive Mermaid diagrams
- **[README.md](./README.md)** - Project overview and setup instructions

## 🎨 Creating Custom Diagrams

If you need to modify or create additional diagrams, the source code is available:

- **`create_visual_diagrams.py`** - Python script using matplotlib for generating PNG diagrams
- **`create_presentation.py`** - Python script using python-pptx for generating PowerPoint presentation

### Requirements for Diagram Generation
```bash
pip install matplotlib seaborn plotly pillow python-pptx
```

### Running the Scripts
```bash
# Generate all PNG diagrams
python create_visual_diagrams.py

# Generate PowerPoint presentation
python create_presentation.py
```

This visual documentation provides a complete graphical representation of the Security Testing API system, making it easy to understand the architecture, flows, and relationships between components.

