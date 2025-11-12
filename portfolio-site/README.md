# Portfolio Site

A responsive single-page site that showcases the three flagship projects in this repository:

1. **Computer Vision Detection App**
2. **Hope Services API**
3. **Hope Services Frontend**

The site is built with vanilla HTML/CSS/JS and designed to be easy to deploy on any static host.

## Preview

Open `index.html` directly in a browser or run a simple static server:

```bash
cd portfolio-site
python -m http.server 8080
# Visit http://localhost:8080
```

## Structure

```
portfolio-site/
├── index.html      # Page markup
├── styles.css      # Global styles + responsive layout
├── script.js       # Mobile nav + scroll animation
└── README.md
```

## Customization

- **Branding**: Update the hero content, name, and social links in `index.html`
- **Projects**: Edit the project cards to point to other repos or change highlights
- **Styling**: Tweaks can be made in `styles.css` (colors, layout, breakpoints)
- **Animations**: Scroll reveal logic lives in `script.js`

## Deployment

Because the site is static, you can deploy it to:

- GitHub Pages
- Netlify / Vercel
- AWS S3 + CloudFront
- Any static site server

Simply upload the contents of `portfolio-site/` to your hosting provider.

## License

MIT
