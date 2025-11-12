import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

export const useCartStore = create(
  persist(
    (set, get) => ({
      items: [],
      
      addItem: (item) => {
        const items = get().items
        const existing = items.find((i) => i.id === item.id)
        
        if (existing) {
          set({
            items: items.map((i) =>
              i.id === item.id
                ? { ...i, quantity: i.quantity + (item.quantity || 1) }
                : i
            ),
          })
        } else {
          set({
            items: [...items, { ...item, quantity: item.quantity || 1 }],
          })
        }
      },
      
      removeItem: (itemId) => {
        set({
          items: get().items.filter((i) => i.id !== itemId),
        })
      },
      
      updateQuantity: (itemId, quantity) => {
        if (quantity <= 0) {
          get().removeItem(itemId)
          return
        }
        
        set({
          items: get().items.map((i) =>
            i.id === itemId ? { ...i, quantity } : i
          ),
        })
      },
      
      clearCart: () => {
        set({ items: [] })
      },
      
      getTotal: () => {
        return get().items.reduce(
          (total, item) => total + parseFloat(item.price) * item.quantity,
          0
        )
      },
    }),
    {
      name: 'hope-services-cart',
      storage: createJSONStorage(() => localStorage),
    }
  )
)

