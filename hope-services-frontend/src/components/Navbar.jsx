import { Link, useNavigate } from 'react-router-dom'
import { ShoppingCart, User, LogOut, Heart, Package } from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import { useCartStore } from '../store/cartStore'

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuthStore()
  const { items } = useCartStore()
  const navigate = useNavigate()
  
  const cartCount = items.reduce((sum, item) => sum + item.quantity, 0)

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <nav className="bg-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <Link to="/" className="text-2xl font-bold text-primary-600">
            Hope Services
          </Link>

          <div className="flex items-center gap-6">
            <Link
              to="/products"
              className="text-gray-700 hover:text-primary-600 transition"
            >
              Products
            </Link>
            <Link
              to="/donations"
              className="flex items-center gap-2 text-gray-700 hover:text-primary-600 transition"
            >
              <Heart className="w-5 h-5" />
              Donate
            </Link>

            <Link
              to="/cart"
              className="relative flex items-center gap-1 text-gray-700 hover:text-primary-600 transition"
            >
              <ShoppingCart className="w-5 h-5" />
              {cartCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  {cartCount}
                </span>
              )}
            </Link>

            {isAuthenticated ? (
              <>
                <Link
                  to="/orders"
                  className="flex items-center gap-2 text-gray-700 hover:text-primary-600 transition"
                >
                  <Package className="w-5 h-5" />
                  Orders
                </Link>
                {user?.role === 'admin' && (
                  <Link
                    to="/admin"
                    className="text-gray-700 hover:text-primary-600 transition"
                  >
                    Admin
                  </Link>
                )}
                <div className="flex items-center gap-3 pl-3 border-l">
                  <span className="text-sm text-gray-600">{user?.name}</span>
                  <button
                    onClick={handleLogout}
                    className="flex items-center gap-1 text-gray-700 hover:text-red-600 transition"
                  >
                    <LogOut className="w-4 h-4" />
                  </button>
                </div>
              </>
            ) : (
              <Link
                to="/login"
                className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition"
              >
                <User className="w-4 h-4" />
                Login
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}


