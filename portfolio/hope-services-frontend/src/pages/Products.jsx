import { useQuery } from '@tanstack/react-query'
import { ShoppingCart } from 'lucide-react'
import api from '../services/api'
import { useCartStore } from '../store/cartStore'
import toast from 'react-hot-toast'

export default function Products() {
  const { data: products = [], isLoading } = useQuery({
    queryKey: ['products'],
    queryFn: async () => {
      const response = await api.get('/inventory/items')
      return response.data
    },
  })

  const addItem = useCartStore((state) => state.addItem)

  const handleAddToCart = (product) => {
    if (product.quantity <= 0) {
      toast.error('Product out of stock')
      return
    }
    addItem(product)
    toast.success(`${product.name} added to cart`)
  }

  if (isLoading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Products</h1>
      <div className="grid md:grid-cols-3 gap-6">
        {products.map((product) => (
          <div
            key={product.id}
            className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition"
          >
            <div className="bg-gradient-to-br from-primary-100 to-primary-200 h-48 flex items-center justify-center">
              <span className="text-4xl">📦</span>
            </div>
            <div className="p-6">
              <h3 className="text-xl font-semibold mb-2">{product.name}</h3>
              <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                {product.description || 'No description available'}
              </p>
              <div className="flex justify-between items-center mb-4">
                <span className="text-2xl font-bold text-primary-600">
                  ${parseFloat(product.price).toFixed(2)}
                </span>
                <span
                  className={`text-sm ${
                    product.quantity > 0 ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  {product.quantity > 0
                    ? `${product.quantity} in stock`
                    : 'Out of stock'}
                </span>
              </div>
              <button
                onClick={() => handleAddToCart(product)}
                disabled={product.quantity <= 0}
                className="w-full bg-primary-600 text-white py-2 rounded-lg font-semibold hover:bg-primary-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                <ShoppingCart className="w-4 h-4" />
                Add to Cart
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}


