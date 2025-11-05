# Datton Services Website

A modern, responsive website for Datton Services showcasing ERP and digital transformation expertise.

## Features

- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Modern UI/UX**: Clean, professional design with smooth animations
- **Interactive Elements**: Hover effects, scroll animations, and form validation
- **Accessibility**: Keyboard navigation and screen reader support
- **Performance Optimized**: Fast loading with optimized assets
- **Contact Form**: Functional contact form with validation
- **Mobile Navigation**: Hamburger menu for mobile devices

## File Structure

```
├── index.html          # Main HTML file
├── styles.css          # CSS styles and responsive design
├── script.js           # JavaScript functionality
└── README.md           # This file
```

## Getting Started

### Prerequisites

- A modern web browser
- A web server (for production deployment)

### Local Development

1. **Download the files**: Save all files in the same directory
2. **Open in browser**: Double-click `index.html` or open it in your browser
3. **Local server** (optional): Use a local server for better development experience

### Using a Local Server

#### Option 1: Python (if installed)
```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

#### Option 2: Node.js (if installed)
```bash
# Install http-server globally
npm install -g http-server

# Run server
http-server
```

#### Option 3: Live Server (VS Code extension)
1. Install "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

## Customization

### Colors and Branding

The website uses a blue color scheme. To change colors, modify these CSS variables in `styles.css`:

```css
/* Primary brand color */
--primary-color: #2563eb;

/* Secondary colors */
--secondary-color: #3b82f6;
--accent-color: #1d4ed8;
```

### Content Updates

#### Company Information
- **Logo**: Update the "Datton" text in the navigation
- **Contact Details**: Modify email, phone, and location in the contact section
- **About Section**: Update company description and statistics

#### Services
Each service card can be customized by editing the content in `index.html`:

```html
<div class="service-card">
    <div class="service-icon">
        <i class="fas fa-[icon-name]"></i>
    </div>
    <h3>Service Title</h3>
    <p>Service description...</p>
    <ul>
        <li>Feature 1</li>
        <li>Feature 2</li>
    </ul>
</div>
```

#### Icons
The website uses Font Awesome icons. Browse available icons at [FontAwesome](https://fontawesome.com/icons) and replace the icon classes.

### Adding New Sections

To add new sections, follow this structure:

```html
<section id="new-section" class="new-section">
    <div class="container">
        <div class="section-header">
            <h2>Section Title</h2>
            <p>Section description</p>
        </div>
        <!-- Section content -->
    </div>
</section>
```

Add corresponding CSS in `styles.css`:

```css
.new-section {
    padding: 80px 0;
    background: #f8fafc;
}
```

## Deployment

### Option 1: Static Hosting (Recommended)

#### Netlify
1. Create a GitHub repository with your website files
2. Connect your repository to Netlify
3. Deploy automatically

#### Vercel
1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in your project directory
3. Follow the prompts

#### GitHub Pages
1. Create a repository named `username.github.io`
2. Upload your website files
3. Enable GitHub Pages in repository settings

### Option 2: Traditional Web Hosting

1. Upload all files to your web hosting provider
2. Ensure `index.html` is in the root directory
3. Test all functionality

### Option 3: Content Management System

You can integrate this design into WordPress, Drupal, or other CMS platforms by:
1. Converting the HTML structure to your CMS template
2. Moving CSS to your theme's stylesheet
3. Converting JavaScript to your CMS's script format

## SEO Optimization

### Meta Tags
Update the `<head>` section in `index.html`:

```html
<meta name="description" content="Datton Services - Expert ERP and digital transformation consulting">
<meta name="keywords" content="ERP, digital transformation, business process management, change management">
<meta name="author" content="Datton Services">
```

### Open Graph Tags
Add these for better social media sharing:

```html
<meta property="og:title" content="Datton Services">
<meta property="og:description" content="Expert ERP and digital transformation consulting">
<meta property="og:image" content="path/to/your/logo.png">
<meta property="og:url" content="https://yourwebsite.com">
```

## Performance Tips

1. **Optimize Images**: Use WebP format and compress images
2. **Minify CSS/JS**: Use tools like UglifyJS or CSS Minifier
3. **Enable Gzip**: Configure your server for compression
4. **Use CDN**: Host Font Awesome and Google Fonts on CDN (already implemented)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Internet Explorer 11+ (with some limitations)

## Troubleshooting

### Common Issues

1. **Fonts not loading**: Check internet connection for Google Fonts
2. **Icons not showing**: Ensure Font Awesome CDN is accessible
3. **Mobile menu not working**: Check JavaScript console for errors
4. **Form not submitting**: Ensure you have a backend service configured

### Debug Mode

Add this to your browser console to enable debug mode:

```javascript
localStorage.setItem('debug', 'true');
```

## Support

For customization help or technical support:

- **Email**: info@datton.com
- **Documentation**: Check this README file
- **Issues**: Create an issue in the repository

## License

This website template is created for Datton Services. Customize as needed for your business requirements.

---

**Datton Services** - Your trusted partner in ERP and digital transformation success.
