import { Link } from 'react-router-dom'
import { Trash2, ShoppingBag } from 'lucide-react'
import { useCartStore } from '../store/cartStore'

export default function Cart() {
  const { items, removeItem, updateQuantity, getTotal } = useCartStore()

  if (items.length === 0) {
    return (
      <div className="text-center py-12">
        <ShoppingBag className="w-24 h-24 text-gray-300 mx-auto mb-4" />
        <h2 className="text-2xl font-bold mb-2">Your cart is empty</h2>
        <p className="text-gray-600 mb-6">Add some items to get started</p>
        <Link
          to="/products"
          className="inline-block bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition"
        >
          Browse Products
        </Link>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Shopping Cart</h1>
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="space-y-4 mb-6">
          {items.map((item) => (
            <div
              key={item.id}
              className="flex items-center justify-between border-b pb-4"
            >
              <div className="flex-1">
                <h3 className="font-semibold">{item.name}</h3>
                <p className="text-gray-600 text-sm">
                  ${parseFloat(item.price).toFixed(2)} each
                </p>
              </div>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => updateQuantity(item.id, item.quantity - 1)}
                    className="w-8 h-8 border rounded-lg hover:bg-gray-100"
                  >
                    -
                  </button>
                  <span className="w-12 text-center">{item.quantity}</span>
                  <button
                    onClick={() => updateQuantity(item.id, item.quantity + 1)}
                    className="w-8 h-8 border rounded-lg hover:bg-gray-100"
                  >
                    +
                  </button>
                </div>
                <div className="w-24 text-right font-semibold">
                  ${(parseFloat(item.price) * item.quantity).toFixed(2)}
                </div>
                <button
                  onClick={() => removeItem(item.id)}
                  className="text-red-600 hover:text-red-700"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="border-t pt-4">
          <div className="flex justify-between items-center mb-4">
            <span className="text-xl font-semibold">Total:</span>
            <span className="text-2xl font-bold text-primary-600">
              ${getTotal().toFixed(2)}
            </span>
          </div>
          <Link
            to="/checkout"
            className="block w-full bg-primary-600 text-white text-center py-3 rounded-lg font-semibold hover:bg-primary-700 transition"
          >
            Proceed to Checkout
          </Link>
        </div>
      </div>
    </div>
  )
}


