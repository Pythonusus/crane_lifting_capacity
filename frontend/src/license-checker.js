class LicenseChecker {
  #jwt = ''
  #fp = ''
  #appExternalId = undefined

  constructor(appExternalId = undefined) {
    const url = new URL(window.location.href)
    this.#jwt = localStorage.getItem('jwt')
    localStorage.setItem('jwt', this.#jwt)
    url.searchParams.delete('jwt')
    window.history.replaceState(null, '', url.toString())

    this.#fp = this.getFingerprint()
    this.#appExternalId = appExternalId
  }

  getFingerprint() {
    // TODO: Better fingerprint
    const userAgent = navigator.userAgent
    const screenRes = `${screen.width}x${screen.height}`
    const timeZone = new Date().getTimezoneOffset()
    const language = navigator.language

    const data = `${userAgent}|${screenRes}|${timeZone}|${language}`

    let hash = 0
    for (let i = 0; i < data.length; i++) {
      const char = data.charCodeAt(i)
      hash = (hash << 5) - hash + char
      hash |= 0 // Convert to 32bit integer
    }

    return hash.toString(36)
  }

  getParams() {
    return {
      jwt: this.#jwt,
      fp: this.#fp,
    }
  }
}

const url = new URL(window.location.href)
const jwt = url.searchParams.get('jwt') || localStorage.getItem('jwt') || ''
localStorage.setItem('jwt', jwt)
url.searchParams.delete('jwt')
window.history.replaceState(null, '', url.toString())
