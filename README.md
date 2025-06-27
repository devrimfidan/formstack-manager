# Formstack Manager

A comprehensive Python-based dashboard for managing and analyzing Formstack forms, folders, and data. Built with Flask, this application provides detailed insights into form usage, analytics, and management capabilities through a modern web interface.

![Formstack Manager Dashboard](https://via.placeholder.com/800x400?text=Formstack+Manager+Dashboard)

## 🚀 Features

### 📊 Dashboard & Analytics
- **Form Overview**: Complete dashboard with form statistics and metrics
- **Analytics & Audit**: Advanced form health scoring and usage analytics
- **Usage Tracking**: Monitor form activity, submissions, and engagement
- **Health Insights**: Identify unused, stale, and dormant forms

### 📁 Organization & Management
- **Folder Management**: Hierarchical folder structure analysis with depth visualization
- **Form Details**: Comprehensive form information with webhooks, integrations, and notifications
- **Smart Search**: Advanced filtering and search capabilities with multiple criteria
- **SmartLists Integration**: Manage and analyze Formstack SmartLists

### 🔍 Advanced Features
- **Partial Submissions Tracking**: Monitor incomplete form submissions
- **Integration Analysis**: View connected services and webhooks
- **Notification Management**: Track email notifications and confirmations
- **Field Analysis**: Detailed form field structure examination
- **Date Range Filtering**: Filter by creation date and last submission date

## 🛠️ Technology Stack

- **Backend**: Python 3.x, Flask
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Data Processing**: Pandas for data analysis
- **API Integration**: Formstack REST API
- **UI Framework**: Font Awesome icons, responsive design

## 📋 Prerequisites

- Python 3.7 or higher
- Formstack API key
- pip package manager

## ⚡ Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/formstack-manager.git
   cd formstack-manager
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   FORMSTACK_API_KEY=your_api_key_here
   ```

4. **Run the application**
   ```bash
   python src/dashboard/app.py
   ```
   Or use the development server:
   ```bash
   python run_server.py
   ```

5. **Access the dashboard**
   Open your browser and navigate to `http://localhost:5006` (or `http://localhost:5001` if using run_server.py)

## 📁 Project Structure

```
formstack-manager/
├── src/
│   ├── api/
│   │   └── formstack_client.py      # Formstack API client
│   ├── analysis/
│   │   ├── folder_analyzer.py       # Folder data analysis
│   │   └── form_analyzer.py         # Form data analysis
│   └── dashboard/
│       ├── app.py                   # Flask application
│       └── templates/               # HTML templates
│           ├── index.html           # Main dashboard
│           ├── audit.html           # Analytics page
│           ├── folders.html         # Folder management
│           ├── form-details.html    # Form details
│           ├── advanced-search.html # Search interface
│           ├── smartlists.html      # SmartLists page
│           └── smartlist-details.html # SmartList details
├── test_*.py                        # API testing scripts
├── main.py                          # Command-line interface
├── run_server.py                    # Development server
├── .env                             # Environment variables (create this)
├── .gitignore                       # Git ignore file
└── README.md
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `FORMSTACK_API_KEY` | Your Formstack API key | Yes |

### API Key Setup

1. Log in to your Formstack account
2. Navigate to Settings → API
3. Generate a new API key
4. Copy the key to your `.env` file

## 📖 Usage Guide

### Dashboard Features

#### 🏠 Main Dashboard (`/`)
- View total forms, submissions, and activity metrics
- Quick access to developer resources
- Real-time statistics updates
- Recent forms overview

#### 📊 Analytics & Audit (`/audit`)
- Form health scoring (percentage of active forms)
- Usage analytics (recent activity, stale forms, dormant forms)
- Actionable insights and recommendations
- Detailed form lifecycle analysis

#### 📁 Folder Management (`/folders`)
- Hierarchical folder structure visualization
- Form distribution across folders
- Folder statistics and metrics
- Sortable and filterable table view
- Column visibility controls

#### 🔍 Advanced Search (`/advanced-search`)
- Multi-criteria form filtering including:
  - Form status (active/inactive)
  - Submissions count ranges
  - Date ranges (created and last submission)
  - Webhooks, confirmations, notifications
  - Partial submissions and integrations
- Export capabilities
- Custom search parameters
- Real-time filtering

#### 📋 Form Details (`/form-details/<form_id>`)
- Comprehensive form information
- Webhook and integration management
- Notification tracking
- Field structure analysis
- Partial submissions overview

#### 📄 SmartLists (`/smartlists`)
- View all SmartLists in your account
- SmartList statistics and overview
- Individual SmartList details

### Command Line Interface

Run reports directly from the command line:

```bash
python main.py
```

This generates a comprehensive form summary report with:
- Form creation dates
- Last submission timestamps
- Folder associations
- Activity metrics

## 🧪 Testing

The project includes comprehensive API testing scripts:

```bash
# Test basic API functionality
python test_api.py

# Test SmartLists API endpoints
python test_smartlists_api.py
```

## 📊 Key Metrics & Analytics

### Form Health Score
Calculated as: `(Forms with Submissions / Total Forms) × 100`

### Activity Categories
- **Active**: Forms with submissions in the last 30 days
- **Stale**: Forms with no submissions in 6+ months
- **Dormant**: Forms inactive for 1+ year
- **Unused**: Forms that have never received submissions

### Insights Generated
- Form health recommendations
- Usage optimization suggestions
- Cleanup candidates identification
- Performance trend analysis

## 🔌 API Integration

The application integrates with multiple Formstack API endpoints:

- **Forms API**: `/api/v2/forms`
- **Folders API**: `/api/v2/folders`
- **Submissions API**: `/api/v2/forms/{id}/submissions`
- **Webhooks API**: `/api/v2/forms/{id}/webhooks`
- **Integrations API**: `/api/v2/forms/{id}/integrations`
- **Confirmations API**: `/api/v2/forms/{id}/confirmations`
- **Notifications API**: `/api/v2/forms/{id}/notifications`
- **SmartLists API**: `/api/v2/smartlists`

## 🏗️ Application Architecture

### Core Components

1. **FormstackClient** (`src/api/formstack_client.py`)
   - Handles all API communications
   - Rate limiting and error handling
   - Authentication management

2. **FormAnalyzer** (`src/analysis/form_analyzer.py`)
   - Processes form data for insights
   - Calculates metrics and statistics
   - Generates summary reports

3. **FolderAnalyzer** (`src/analysis/folder_analyzer.py`)
   - Analyzes folder hierarchy
   - Calculates folder statistics
   - Manages folder relationships

4. **Flask Application** (`src/dashboard/app.py`)
   - Web interface and routing
   - Template rendering
   - API endpoints for frontend

### Key Features by Page

| Page | Key Features | Purpose |
|------|-------------|---------|
| Dashboard | Overview stats, recent forms | Quick health check |
| Audit | Analytics cards, insights | Deep analysis |
| Folders | Hierarchy view, statistics | Organization management |
| Advanced Search | Multi-filter search, export | Detailed form discovery |
| Form Details | Complete form information | Individual form analysis |
| SmartLists | SmartList management | Data collection insights |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Developer**: Emin Devrim Fidan
- **AI Assistant**: GitHub Copilot for development assistance
- **Framework**: Flask for the web application framework
- **UI**: Tailwind CSS for responsive design
- **Icons**: Font Awesome for the icon library

## 🐛 Known Issues & Limitations

- API rate limiting may affect large-scale data retrieval
- Some Formstack features may require specific account permissions
- Date parsing assumes specific Formstack date formats

## 🔮 Future Enhancements

- [ ] Export functionality for analytics reports
- [ ] Email notifications for form health alerts
- [ ] Scheduled automated reports
- [ ] Integration with external analytics platforms
- [ ] Multi-account support
- [ ] Advanced visualization charts
- [ ] Form performance tracking
- [ ] Automated cleanup recommendations
- [ ] Dashboard customization options

## 📞 Support

For issues and questions:
1. Check the [Issues](https://github.com/yourusername/formstack-manager/issues) page
2. Create a new issue with detailed information
3. Include error messages and system information

## 🔒 Security

- API keys are stored in environment variables
- No sensitive data is logged or exposed
- All API communications use HTTPS
- Follow Formstack's API usage guidelines

## 🌟 Show Your Support

If this project helps you manage your Formstack forms more effectively, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 🤝 Contributing to the codebase

---

**Built with ❤️ for the Formstack community**

*Transform your form management experience with powerful analytics and insights.*