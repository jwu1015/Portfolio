import { useQuery } from '@tanstack/react-query'
import { Package, Calendar } from 'lucide-react'
import api from '../services/api'

export default function Orders() {
  const { data: orders = [], isLoading } = useQuery({
    queryKey: ['orders'],
    queryFn: async () => {
      // Note: API would need an orders endpoint
      // For now, returning empty array
      return []
    },
    enabled: false, // Disable until endpoint exists
  })

  if (isLoading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
      </div>
    )
  }

  if (orders.length === 0) {
    return (
      <div className="text-center py-12">
        <Package className="w-24 h-24 text-gray-300 mx-auto mb-4" />
        <h2 className="text-2xl font-bold mb-2">No orders yet</h2>
        <p className="text-gray-600">Your order history will appear here</p>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">My Orders</h1>
      <div className="space-y-4">
        {orders.map((order) => (
          <div key={order.id} className="bg-white rounded-lg shadow-md p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-xl font-semibold">Order #{order.id}</h3>
                <p className="text-gray-600 flex items-center gap-2 mt-1">
                  <Calendar className="w-4 h-4" />
                  {new Date(order.created_at).toLocaleDateString()}
                </p>
              </div>
              <span
                className={`px-3 py-1 rounded-full text-sm font-semibold ${
                  order.status === 'completed'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-yellow-100 text-yellow-800'
                }`}
              >
                {order.status}
              </span>
            </div>
            <div className="border-t pt-4">
              <div className="flex justify-between">
                <span className="text-gray-600">Total:</span>
                <span className="text-xl font-bold">
                  ${parseFloat(order.total_amount).toFixed(2)}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}


