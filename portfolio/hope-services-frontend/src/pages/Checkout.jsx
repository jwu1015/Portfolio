import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCartStore } from '../store/cartStore'
import { generateIdempotencyKey, storeIdempotencyKey } from '../utils/idempotency'
import api from '../services/api'
import toast from 'react-hot-toast'
import { CheckCircle } from 'lucide-react'

export default function Checkout() {
  const { items, getTotal, clearCart } = useCartStore()
  const [shippingAddress, setShippingAddress] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const idempotencyKey = generateIdempotencyKey()
      storeIdempotencyKey('last-order', idempotencyKey)

      const orderData = {
        items: items.map((item) => ({
          inventory_item_id: item.id,
          quantity: item.quantity,
        })),
        shipping_address: shippingAddress,
      }

      const response = await api.post('/orders', orderData, {
        headers: {
          'Idempotency-Key': idempotencyKey,
        },
      })

      toast.success('Order placed successfully!')
      clearCart()
      navigate('/orders')
    } catch (error) {
      toast.error(error.response?.data?.error || 'Failed to place order')
    }

    setLoading(false)
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Checkout</h1>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Order Summary</h2>
          <div className="space-y-2 mb-4">
            {items.map((item) => (
              <div key={item.id} className="flex justify-between">
                <span>
                  {item.name} x {item.quantity}
                </span>
                <span>${(parseFloat(item.price) * item.quantity).toFixed(2)}</span>
              </div>
            ))}
          </div>
          <div className="border-t pt-4 flex justify-between text-xl font-bold">
            <span>Total:</span>
            <span className="text-primary-600">${getTotal().toFixed(2)}</span>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Shipping Address</h2>
          <textarea
            value={shippingAddress}
            onChange={(e) => setShippingAddress(e.target.value)}
            placeholder="Enter your shipping address"
            rows={4}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>

        <button
          type="submit"
          disabled={loading || items.length === 0}
          className="w-full bg-primary-600 text-white py-3 rounded-lg font-semibold hover:bg-primary-700 transition disabled:opacity-50 flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              Placing Order...
            </>
          ) : (
            <>
              <CheckCircle className="w-5 h-5" />
              Place Order
            </>
          )}
        </button>
      </form>
    </div>
  )
}


