export default {
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.(js|jsx)$': 'babel-jest',
  },
  extensionsToTreatAsEsm: ['.jsx'],
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': '<rootDir>/__mocks__/styleMock.js',
    '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$':
      '<rootDir>/__mocks__/fileMock.js',
  },
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],

  // Coverage configuration
  collectCoverageFrom: [
    '**/src/**.{js,jsx}',
    '!**/*.test.{js,jsx}',
    '!**/__tests__/**',
    '!**/node_modules/**',
    '!**/coverage/**',
    '!src/main.jsx',
  ],
  coverageReporters: ['text', 'lcov', 'html'],
}
