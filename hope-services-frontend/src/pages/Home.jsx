import { Link } from 'react-router-dom'
import { ShoppingBag, Heart, ArrowRight } from 'lucide-react'

export default function Home() {
  return (
    <div>
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 text-white rounded-2xl p-12 mb-8 text-center">
        <h1 className="text-5xl font-bold mb-4">Welcome to Hope Services</h1>
        <p className="text-xl mb-8 opacity-90">
          Making a difference through commerce and compassion
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            to="/products"
            className="bg-white text-primary-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition flex items-center gap-2"
          >
            <ShoppingBag className="w-5 h-5" />
            Shop Now
          </Link>
          <Link
            to="/donations"
            className="bg-primary-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-400 transition flex items-center gap-2"
          >
            <Heart className="w-5 h-5" />
            Donate
          </Link>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <ShoppingBag className="w-12 h-12 text-primary-600 mb-4" />
          <h3 className="text-xl font-semibold mb-2">Shop Essentials</h3>
          <p className="text-gray-600 mb-4">
            Browse our catalog of essential items for those in need
          </p>
          <Link
            to="/products"
            className="text-primary-600 hover:text-primary-700 flex items-center gap-1"
          >
            Explore <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <Heart className="w-12 h-12 text-red-500 mb-4" />
          <h3 className="text-xl font-semibold mb-2">Make a Difference</h3>
          <p className="text-gray-600 mb-4">
            Support our mission with a donation. Every contribution helps.
          </p>
          <Link
            to="/donations"
            className="text-primary-600 hover:text-primary-700 flex items-center gap-1"
          >
            Donate <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <ArrowRight className="w-12 h-12 text-green-500 mb-4" />
          <h3 className="text-xl font-semibold mb-2">Get Started</h3>
          <p className="text-gray-600 mb-4">
            Create an account to track orders and manage your account
          </p>
          <Link
            to="/login"
            className="text-primary-600 hover:text-primary-700 flex items-center gap-1"
          >
            Sign Up <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </div>
  )
}


