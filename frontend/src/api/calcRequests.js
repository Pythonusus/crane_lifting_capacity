/**
 * Create a base payload calculation request
 * @param {string} craneName - Name of the crane
 * @param {string} boomLen - Boom length configuration
 * @param {string} radius - Radius in meters (as string)
 * @param {number} equipmentWeight - Weight of equipment in tons
 * @param {number} safetyFactor - Safety factor
 * @returns {Object} Base payload request object
 */
export const createPayloadBaseRequest = (
  craneName,
  boomLen,
  radius,
  equipmentWeight,
  safetyFactor,
) => ({
  crane_name: craneName,
  boom_len: boomLen,
  radius: radius, // Send as string, no need to parse
  equipment_weight: Number.parseFloat(equipmentWeight),
  safety_factor: Number.parseFloat(safetyFactor),
})

/**
 * Create a base safety factor calculation request
 * @param {string} craneName - Name of the crane
 * @param {string} boomLen - Boom length configuration
 * @param {string} radius - Radius in meters (as string)
 * @param {number} equipmentWeight - Weight of equipment in tons
 * @param {number} payload - Desired payload in tons
 * @returns {Object} Base safety factor request object
 */
export const createSafetyFactorBaseRequest = (
  craneName,
  boomLen,
  radius,
  equipmentWeight,
  payload,
) => ({
  crane_name: craneName,
  boom_len: boomLen,
  radius: radius,
  equipment_weight: Number.parseFloat(equipmentWeight),
  payload: Number.parseFloat(payload),
})

/**
 * Calculate payload for given base requests
 * @param {...Object} baseRequests - Any number of base payload requests
 * @returns {Promise<Object>} Calculation results
 */
export const calculatePayload = async (...baseRequests) => {
  const payloadRequest = {
    payload_request: {
      base_requests: baseRequests,
    },
  }

  const response = await fetch('/process', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payloadRequest),
  })

  if (!response.ok) {
    throw new Error('Failed to calculate payload')
  }

  return await response.json()
}

/**
 * Calculate safety factor for given base requests
 * @param {...Object} baseRequests - Any number of base safety factor requests
 * @returns {Promise<Object>} Calculation results
 */
export const calculateSafetyFactor = async (...baseRequests) => {
  const safetyRequest = {
    safety_request: {
      base_requests: baseRequests,
    },
  }

  const response = await fetch('/process', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(safetyRequest),
  })

  if (!response.ok) {
    throw new Error('Ошибка в расчете коэффициента запаса')
  }

  return await response.json()
}
