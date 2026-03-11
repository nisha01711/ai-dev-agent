# AI Dev Agent - Frontend

A modern, responsive React frontend for the AI Software Engineer Platform.

## Features

- 🎨 Modern dark theme with professional developer UI
- ⚡ Built with React + Vite for fast development
- 💅 Styled with Tailwind CSS
- 🎯 Multi-page application with React Router
- 📱 Fully responsive mobile layout
- 🚀 AI-powered task planning and code generation interface
- 📊 Architecture visualization
- 📝 Task history tracking
- ⚙️ Settings and configuration

## Technology Stack

- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Routing**: React Router v6
- **Code Display**: Prism.js

## Getting Started

### Prerequisites

- Node.js 16+ installed
- npm or yarn package manager

### Installation

1. Navigate to the Frontend directory:
```bash
cd Frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will open at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

## Project Structure

```
Frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Navbar.jsx
│   │   ├── Sidebar.jsx
│   │   ├── FeatureCard.jsx
│   │   ├── TaskInput.jsx
│   │   ├── CodeViewer.jsx
│   │   ├── TerminalOutput.jsx
│   │   ├── ArchitectureDiagram.jsx
│   │   ├── LoadingSpinner.jsx
│   │   └── StepProgress.jsx
│   ├── pages/               # Page components
│   │   ├── Landing.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Architecture.jsx
│   │   ├── TaskHistory.jsx
│   │   └── Settings.jsx
│   ├── App.jsx              # Main app component with routing
│   ├── main.jsx             # Application entry point
│   └── index.css            # Global styles
├── public/                  # Static assets
├── index.html              # HTML template
├── package.json            # Dependencies and scripts
├── vite.config.js          # Vite configuration
├── tailwind.config.js      # Tailwind CSS configuration
└── postcss.config.js       # PostCSS configuration
```

## Available Pages

### 1. Landing Page (`/`)
- Hero section with product introduction
- Feature cards showcasing AI capabilities
- How it works section
- Call-to-action buttons

### 2. Dashboard (`/dashboard`)
- Task input for AI processing
- AI planning output with step progress
- Generated code viewer with syntax highlighting
- Execution logs in terminal-style output
- AI debug suggestions

### 3. Architecture View (`/architecture`)
- Visual system architecture diagram
- Technology stack details
- Performance metrics

### 4. Task History (`/history`)
- Table of all previous tasks
- Search and filter functionality
- Task statistics overview
- Quick access to reopen tasks

### 5. Settings (`/settings`)
- Profile configuration
- Notification preferences
- AI model selection
- Default language settings

## Key Components

### Navbar
Top navigation bar with routing links and menu toggle for mobile.

### Sidebar
Left sidebar navigation (collapsible on mobile) with:
- New Task button
- Navigation links
- AI status indicator

### TaskInput
Text area component for entering software tasks with submit button.

### CodeViewer
Syntax-highlighted code display with:
- File name header
- Language indicator
- Copy to clipboard functionality

### TerminalOutput
Terminal-style log viewer with:
- Colored log levels (info, success, error)
- Timestamps
- Auto-scroll

### ArchitectureDiagram
Visual representation of system architecture with:
- Component cards
- Connection arrows
- Interactive hover effects

## Styling

The application uses a custom dark theme with:
- Primary background: `#0a0a0a`
- Secondary background: `#1a1a1a`
- Tertiary background: `#2a2a2a`
- Accent colors: Blue, Purple, Green, Red
- Custom scrollbar styling
- Glass morphism effects
- Gradient text

## Customization

### Colors
Edit `tailwind.config.js` to modify the color scheme:
```javascript
colors: {
  dark: {
    primary: '#0a0a0a',
    secondary: '#1a1a1a',
    // ... more colors
  }
}
```

### Fonts
Add or change fonts in `src/index.css` by importing Google Fonts.

## Development Tips

- Use the React DevTools browser extension for debugging
- Hot Module Replacement (HMR) is enabled for instant updates
- Check browser console for any errors or warnings
- Use the responsive design mode in browser DevTools to test mobile layouts

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## License

MIT License - feel free to use this in your projects!
