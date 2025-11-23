# Hope Services Frontend

Modern React frontend for the Hope Services e-commerce and donations platform.

## Features

- **Product Browsing**: Browse inventory items with filtering
- **Shopping Cart**: Add items, update quantities, remove items
- **Checkout Flow**: Secure checkout with idempotency support
- **Donations**: Make one-time or recurring donations
- **Order History**: View past orders and status
- **Admin Dashboard**: Manage inventory (for admin users)
- **Authentication**: JWT-based login system
- **Responsive Design**: Mobile-friendly UI

## Tech Stack

- React 18
- React Router v6
- TanStack Query (React Query)
- Zustand (State management)
- Tailwind CSS
- Vite
- Axios

## Quick Start

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

Frontend runs on `http://localhost:3000`

The app proxies API requests to `http://localhost:5000`

### Build

```bash
npm run build
```

### Production

After building, serve the `dist/` folder with any static file server.

## Configuration

Update `vite.config.js` to change API proxy target:

```js
proxy: {
  '/api': {
    target: 'http://your-api-url:5000',
    changeOrigin: true,
  }
}
```

## Default Test Accounts

- **Customer**: customer@example.com / password123
- **Admin**: admin@hope.org / admin123

## Project Structure

```
src/
├── components/        # Reusable components
│   ├── Navbar.jsx
│   └── ProtectedRoute.jsx
├── pages/            # Page components
│   ├── Home.jsx
│   ├── Products.jsx
│   ├── Cart.jsx
│   ├── Checkout.jsx
│   ├── Orders.jsx
│   ├── Donations.jsx
│   ├── Admin.jsx
│   └── Login.jsx
├── store/            # Zustand stores
│   ├── authStore.js
│   └── cartStore.js
├── services/         # API services
│   └── api.js
└── utils/           # Utilities
    └── idempotency.js
```

## Features in Detail

### Shopping Cart
- Persistent cart using Zustand with localStorage
- Add/remove items
- Update quantities
- Calculate totals

### Checkout
- Idempotency key generation
- Prevents duplicate orders
- Shipping address input
- Order confirmation

### Admin Dashboard
- View all products
- Add new products
- Edit/delete products (UI ready, API integration needed)

### Donations
- One-time or recurring donations
- Amount input with validation
- Donation confirmation

## License

MIT


