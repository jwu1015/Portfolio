import { useState } from 'react'
import { Heart } from 'lucide-react'
import api from '../services/api'
import toast from 'react-hot-toast'

export default function Donations() {
  const [amount, setAmount] = useState('')
  const [donationType, setDonationType] = useState('one-time')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      await api.post('/donations', {
        amount: parseFloat(amount),
        donation_type: donationType,
        payment_method: 'credit_card',
      })

      toast.success('Thank you for your donation!')
      setAmount('')
    } catch (error) {
      toast.error(error.response?.data?.error || 'Donation failed')
    }

    setLoading(false)
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <Heart className="w-16 h-16 text-red-500 mx-auto mb-4" />
        <h1 className="text-4xl font-bold mb-4">Make a Donation</h1>
        <p className="text-gray-600 text-lg">
          Your contribution helps us serve those in need
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Donation Amount
            </label>
            <div className="relative">
              <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">
                $
              </span>
              <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
                min="0.01"
                step="0.01"
                className="w-full pl-8 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-lg"
                placeholder="0.00"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Donation Type
            </label>
            <select
              value={donationType}
              onChange={(e) => setDonationType(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="one-time">One-time</option>
              <option value="recurring">Recurring (Monthly)</option>
              <option value="annual">Annual</option>
            </select>
          </div>

          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">
              <strong>Note:</strong> This is a demo application. No actual payment
              processing is performed.
            </p>
          </div>

          <button
            type="submit"
            disabled={loading || !amount || parseFloat(amount) <= 0}
            className="w-full bg-red-500 text-white py-3 rounded-lg font-semibold hover:bg-red-600 transition disabled:opacity-50 flex items-center justify-center gap-2"
          >
            <Heart className="w-5 h-5" />
            {loading ? 'Processing...' : 'Donate Now'}
          </button>
        </form>
      </div>
    </div>
  )
}


