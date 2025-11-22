---
title: "Hope Services Frontend"
date: "2025-01-25"
summary: "Modern React e-commerce storefront with shopping cart, checkout, donations, and admin dashboard built with Vite and Tailwind CSS"
tags: ["react", "typescript", "vite", "tailwindcss", "zustand", "tanstack-query", "e-commerce"]
cover: "/images/projects/hope-frontend-cover.jpg"
links:
  demo: "https://hope-services-store.netlify.app"
  code: "https://github.com/yourusername/Portfolio/tree/main/hope-services-frontend"
published: true
---

Built a polished, responsive React storefront that delivers seamless shopping experiences for customers and powerful admin tooling for inventory management. The application uses Zustand for persistent cart and authentication state, TanStack Query for efficient API communication, and Tailwind CSS for scalable theming. The checkout flow implements idempotency key generation to prevent duplicate orders, while the donations interface supports one-time and recurring contributions. The admin dashboard provides full CRUD operations for inventory management, with real-time updates and toast notifications for user feedback.

**Key Features:**
- 8 production pages: Home, Products, Cart, Checkout, Orders, Donations, Admin, Login
- Persistent shopping cart and authentication with localStorage
- Protected routes with role-based access control (admin vs customer)
- Idempotency key helpers for safe order creation
- Responsive design with mobile-first approach
- API integration with error handling and loading states
- Toast notifications for user feedback

**My Role:** Frontend architect, Product designer

**Impact:** Created a complete e-commerce experience that demonstrates modern React patterns and best practices. The state management approach ensures data persistence across sessions, while the component architecture makes it easy to extend and maintain. The admin dashboard enables non-technical users to manage inventory without touching the backend directly.

**Technical Highlight:** Implemented a custom idempotency utility that generates unique keys per order attempt and stores them in localStorage, ensuring that retries (due to network issues) don't result in duplicate charges. This pattern can be extended to any critical transaction flow.

