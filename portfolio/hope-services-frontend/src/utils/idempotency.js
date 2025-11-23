export function generateIdempotencyKey() {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}

export function getIdempotencyKeyFromStorage(orderKey) {
  const key = localStorage.getItem(`idempotency-${orderKey}`)
  if (key) {
    const data = JSON.parse(key)
    // Key expires after 24 hours
    if (Date.now() - data.timestamp < 24 * 60 * 60 * 1000) {
      return data.key
    }
  }
  return null
}

export function storeIdempotencyKey(orderKey, key) {
  localStorage.setItem(
    `idempotency-${orderKey}`,
    JSON.stringify({
      key,
      timestamp: Date.now(),
    })
  )
}


