import js from '@eslint/js'
import prettierConfig from 'eslint-config-prettier'
import xo from 'eslint-config-xo'
import xoReact from 'eslint-config-xo-react'
import htmlPlugin from 'eslint-plugin-html'
import importPlugin from 'eslint-plugin-import'
import jestPlugin from 'eslint-plugin-jest'
import jsxA11y from 'eslint-plugin-jsx-a11y'
import prettierPlugin from 'eslint-plugin-prettier'
import promisePlugin from 'eslint-plugin-promise'
import reactPlugin from 'eslint-plugin-react'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import securityPlugin from 'eslint-plugin-security'
import sonarjsPlugin from 'eslint-plugin-sonarjs'
import testingLibrary from 'eslint-plugin-testing-library'
import unicornPlugin from 'eslint-plugin-unicorn'
import globals from 'globals'

export default [
  {
    ignores: [
      'dist/**',
      'build/**',
      'node_modules/**',
      '.git/**',
      '.cache/**',
      '.npm/**',
      '*.log',
      '.idea/**',
      '.vscode/**',
      '*.sw?',
      '.DS_Store',
      '**/*.css',
      '*/coverage/**',
      'coverage/**',
      'public/**',
      'storybook-static/**',
      '.next/**',
      'out/**',
      '.docusaurus/**',
      '*.min.js',
      '**/*.d.ts',
      'stats.json',
      'cypress/screenshots/**',
      'cypress/videos/**',
      'tmp/**',
      '.nyc_output/**',
      'docs/api/**',
    ],
  },
  {
    files: ['**/*.{js,jsx}'],
    languageOptions: {
      ecmaVersion: 2022,
      globals: {
        ...globals.browser,
        ...globals.jest,
        ...globals.node,
      },
      parserOptions: {
        ecmaVersion: 'latest',
        ecmaFeatures: { jsx: true },
        sourceType: 'module',
      },
    },
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
      react: reactPlugin,
      prettier: prettierPlugin,
      import: importPlugin,
      'jsx-a11y': jsxA11y,
      promise: promisePlugin,
      unicorn: unicornPlugin,
      sonarjs: sonarjsPlugin,
      security: securityPlugin,
    },
    rules: {
      ...js.configs.recommended.rules,
      ...xo.rules,
      ...xoReact.rules,
      ...reactHooks.configs.recommended.rules,
      ...prettierConfig.rules,
      ...promisePlugin.configs.recommended.rules,
      ...unicornPlugin.configs.recommended.rules,
      ...sonarjsPlugin.configs.recommended.rules,
      ...securityPlugin.configs.recommended.rules,

      // Prettier
      'prettier/prettier': ['error'],

      // React
      'react/react-in-jsx-scope': 'off',
      'react/jsx-uses-react': 'off',

      // JavaScript
      'no-unused-vars': ['error', { varsIgnorePattern: '^[A-Z]' }],

      // React Refresh
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true },
      ],

      // Import
      'import/order': [
        'error',
        {
          groups: [
            'builtin',
            'external',
            'internal',
            'parent',
            'sibling',
            'index',
          ],
          'newlines-between': 'always',
          alphabetize: { order: 'asc', caseInsensitive: true },
        },
      ],

      // JSX-a11y plugin rules
      ...jsxA11y.configs.recommended.rules,

      // Promise
      'promise/always-return': 'warn',
      'promise/no-return-wrap': 'error',
      'promise/param-names': 'error',

      // Unicorn - disable rules that conflict with React patterns
      'unicorn/filename-case': 'off',
      'unicorn/prevent-abbreviations': 'off',
      'unicorn/no-null': 'off',
      'unicorn/no-array-reduce': 'off',
    },
  },
  // Jest test files configuration
  {
    files: ['**/*.{test,spec}.{js,jsx}', '**/__tests__/**/*.{js,jsx}'],
    plugins: {
      jest: jestPlugin,
      'testing-library': testingLibrary,
    },
    languageOptions: {
      globals: {
        ...globals.jest,
      },
    },
    rules: {
      // Jest plugin rules
      ...jestPlugin.configs.recommended.rules,
      // Testing Library rules
      ...testingLibrary.configs.react.rules,

      // Disable some rules that are problematic in test files
      'import/no-extraneous-dependencies': 'off',
      'sonarjs/no-duplicate-string': 'off',
      'sonarjs/no-identical-functions': 'off',
      'unicorn/consistent-function-scoping': 'off',

      // Additional Jest-specific rules
      'jest/no-disabled-tests': 'warn',
      'jest/no-focused-tests': 'error',
      'jest/no-identical-title': 'error',
      'jest/valid-expect': 'error',
      'jest/expect-expect': 'error',
    },
  },
  {
    files: ['**/*.html'],
    plugins: {
      html: htmlPlugin,
      prettier: prettierPlugin,
    },
    languageOptions: {
      globals: globals.browser,
    },
    rules: {
      'max-len': 'off',
      'prettier/prettier': ['error', { parser: 'html' }],
    },
  },
]
