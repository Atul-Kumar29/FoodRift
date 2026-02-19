# AgriTrust Frontend

React-based frontend application for the AgriTrust blockchain food safety and traceability system.

## Overview

This frontend provides a user interface for interacting with the FoodSafetyApp smart contract on Algorand. It enables users to manage food batch lifecycles, upload documents to IPFS, and connect using multiple wallet providers.

## Features

- **Food Safety Operations**: Create, inspect, distribute, and recall food batches
- **Wallet Integration**: Support for Pera Wallet and Local Wallet (KMD)
- **IPFS Document Storage**: Upload and view inspection documents and batch information
- **Real-time Updates**: Query batch information and view transaction history
- **Responsive Design**: Mobile-friendly interface built with Tailwind CSS

---

## Setup

### Prerequisites

- **Node.js**: Version 18+ required. Verify with `npm -v`
- **AlgoKit CLI**: Version 2.0.0+. Install from [AlgoKit CLI Installation Guide](https://github.com/algorandfoundation/algokit-cli#install)

### Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd projects/frontend
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```
   
   Or using AlgoKit from the workspace root:
   ```bash
   algokit project bootstrap all
   ```

3. **Configure Environment**
   
   Create a `.env` file based on `.env.template`:
   ```bash
   cp .env.template .env
   ```
   
   Edit `.env` with your configuration (see Environment Variables section below)

4. **Start Development Server**
   ```bash
   npm run dev
   ```
   
   The application will be available at `http://localhost:5173`

---

## Environment Variables

The application requires the following environment variables in the `.env` file:

### Network Configuration

```bash
# Algod (Algorand node)
VITE_ALGOD_SERVER=https://testnet-api.algonode.cloud
VITE_ALGOD_PORT=
VITE_ALGOD_TOKEN=
VITE_ALGOD_NETWORK=testnet

# Indexer (for querying blockchain data)
VITE_INDEXER_SERVER=https://testnet-idx.algonode.cloud
VITE_INDEXER_PORT=
VITE_INDEXER_TOKEN=
```

### Local Wallet (KMD) - Optional

Only required if using Local Wallet for development:

```bash
VITE_KMD_SERVER=http://localhost
VITE_KMD_PORT=4002
VITE_KMD_TOKEN=a-super-secret-token
VITE_KMD_WALLET=unencrypted-default-wallet
VITE_KMD_PASSWORD=some-password
```

### IPFS Configuration

Required for document uploads:

```bash
# Pinata JWT token (get from https://app.pinata.cloud/developers/api-keys)
VITE_PINATA_JWT=eyJhbGciOi...

# Optional: Custom IPFS gateway
VITE_PINATA_GATEWAY=https://gateway.pinata.cloud/ipfs
```

**Note:** Restart the dev server after modifying `.env` variables.

---

## Wallet Integration

### Supported Wallets

The application supports two wallet providers:

#### 1. Pera Wallet

**Description:** Mobile and web wallet for Algorand with secure transaction signing.

**Setup:**
1. Install Pera Wallet from [https://perawallet.app](https://perawallet.app)
2. Create or import an account
3. In the app, click "Connect Wallet" and select "Pera Wallet"
4. Approve the connection in your Pera Wallet app/extension

**Features:**
- Mobile app (iOS/Android) and browser extension
- QR code connection
- Multi-account support
- Secure key management

#### 2. Local Wallet (KMD)

**Description:** Development wallet using Algorand's Key Management Daemon.

**Setup:**
1. Start AlgoKit LocalNet: `algokit localnet start`
2. Configure KMD environment variables in `.env`
3. In the app, click "Connect Wallet" and select "Local Wallet"
4. Choose an account from the list

**Features:**
- Best for local development and testing
- Fast transaction signing
- No mobile app required
- Works with AlgoKit LocalNet

### Wallet Provider Configuration

The wallet providers are configured in `src/App.tsx` using the `@txnlab/use-wallet-react` library:

```typescript
import { WalletProvider, WalletId } from '@txnlab/use-wallet-react'
import { PeraWalletConnect } from '@perawallet/connect'

const walletManager = new WalletManager({
  wallets: [
    {
      id: WalletId.PERA,
      options: { clientStatic: PeraWalletConnect }
    },
    {
      id: WalletId.KMD,
      options: { /* KMD configuration */ }
    }
  ]
})
```

---

## Project Structure

```
src/
├── components/
│   ├── FoodSafety.tsx        # Main food safety operations
│   ├── ConnectWallet.tsx     # Wallet connection modal
│   ├── Account.tsx           # Wallet account display
│   └── ErrorBoundary.tsx     # Error handling wrapper
├── contracts/
│   └── FoodSafetyApp.ts      # Generated contract client
├── utils/
│   ├── pinata.ts             # IPFS integration
│   └── network/
│       └── getAlgoClientConfigs.ts  # Network configuration
├── App.tsx                   # Main app component with wallet setup
├── Home.tsx                  # Landing page
└── main.tsx                  # Application entry point
```

---

## Development Workflow

### Build Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linting
npm run lint

# Run tests
npm test

# Run end-to-end tests
npm run test:e2e
```

### AlgoKit Integration

When working in an AlgoKit workspace, you can use:

```bash
# Build all projects (from workspace root)
algokit project run build

# Run frontend dev server (from workspace root)
algokit project run frontend
```

---

## Smart Contract Integration

### Generated Contract Clients

The frontend uses TypeScript clients generated from smart contract artifacts. These clients are located in `src/contracts/` and provide type-safe interfaces for contract interactions.

**Generating Clients:**

When smart contracts are updated, regenerate the TypeScript clients:

```bash
algokit generate client
```

### Contract Operations

The `FoodSafety.tsx` component demonstrates how to interact with the FoodSafetyApp contract:

**Create Batch:**
```typescript
await appClient.createBatch({
  batchId: 'BATCH001',
  producerAddress: walletAddress,
  productName: 'Organic Apples',
  originLocation: 'Farm A',
  harvestDate: BigInt(Date.now()),
  ipfsHash: 'QmXxx...'
})
```

**Inspect Batch:**
```typescript
await appClient.inspectBatch({
  batchId: 'BATCH001',
  inspectionReportHash: 'QmYyy...',
  approved: true
})
```

**Query Batch:**
```typescript
const batch = await appClient.getBatch({
  batchId: 'BATCH001'
})
```

---

## IPFS Integration

### Pinata Setup

1. Create a Pinata account at [https://app.pinata.cloud](https://app.pinata.cloud)
2. Generate an API Key/JWT at [https://app.pinata.cloud/developers/api-keys](https://app.pinata.cloud/developers/api-keys)
3. Add the JWT to `.env` as `VITE_PINATA_JWT`

### Upload Functions

The `src/utils/pinata.ts` file provides utilities for uploading to IPFS:

**Upload File:**
```typescript
import { pinFileToIPFS } from './utils/pinata'

const result = await pinFileToIPFS(file)
console.log('IPFS Hash:', result.IpfsHash)
```

**Upload JSON:**
```typescript
import { pinJSONToIPFS } from './utils/pinata'

const result = await pinJSONToIPFS({ 
  name: 'Batch Data',
  data: { /* batch information */ }
})
console.log('IPFS Hash:', result.IpfsHash)
```

### Viewing Documents

IPFS hashes are displayed as clickable links in the UI. The gateway URL is configured via `VITE_PINATA_GATEWAY` or defaults to `https://ipfs.io/ipfs`.

---

## Testing

### Unit Tests

Run unit tests with Jest:

```bash
npm test
```

Tests are located in `tests/` and use the `.test.ts` or `.test.tsx` extension.

### End-to-End Tests

Run E2E tests with Playwright:

```bash
npm run test:e2e
```

E2E tests are located in `tests/` and use the `.spec.ts` extension.

### Test Configuration

- **Jest Config**: `jest.config.ts`
- **Playwright Config**: `playwright.config.ts`

---

## Continuous Integration

### GitHub Actions

The project includes CI workflows in `.github/workflows/` that run on pull requests and pushes to `main`:

**Checks:**
- Install dependencies
- Lint code with ESLint
- Build application with Vite
- Run tests

### Continuous Deployment

The project supports deployment to Netlify or Vercel.

#### Netlify Deployment

1. **Setup:**
   - Create Netlify account
   - Generate [Netlify Access Token](https://docs.netlify.com/cli/get-started/#obtain-a-token-in-the-netlify-ui)
   - Run `netlify login` and `netlify sites:create`
   - Add `NETLIFY_AUTH_TOKEN` and `NETLIFY_SITE_ID` to GitHub secrets

2. **Environment Variables:**
   - Configure `VITE_*` environment variables in Netlify site settings

3. **Deploy:**
   - Push to `main` branch triggers automatic deployment

#### Vercel Deployment

1. **Setup:**
   - Create Vercel account
   - Generate [Vercel Access Token](https://vercel.com/support/articles/how-do-i-use-a-vercel-api-access-token)
   - Run `vercel login` and `vercel link`
   - Add `VERCEL_TOKEN`, `VERCEL_ORG_ID`, and `VERCEL_PROJECT_ID` to GitHub secrets

2. **Environment Variables:**
   - Upload `.env` file to Vercel project or configure via dashboard

3. **Deploy:**
   - Push to `main` branch triggers automatic deployment

---

## Technology Stack

### Core Technologies

- **React 18**: UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Build tool and dev server

### Styling

- **Tailwind CSS**: Utility-first CSS framework
- **DaisyUI**: Component library for Tailwind

### Algorand Integration

- **@algorandfoundation/algokit-utils**: Algorand utilities
- **@txnlab/use-wallet-react**: Wallet integration hook
- **@perawallet/connect**: Pera Wallet provider
- **algosdk**: Algorand JavaScript SDK

### Additional Libraries

- **notistack**: Toast notifications
- **react-router-dom**: Routing (if applicable)

### Development Tools

- **ESLint**: Code linting
- **Prettier**: Code formatting
- **Jest**: Unit testing
- **Playwright**: E2E testing

---

## Troubleshooting

### Common Issues

**"Missing VITE_ALGOD_SERVER"**
- Ensure `.env` file exists in `projects/frontend`
- Verify all required variables are set
- Restart dev server: `npm run dev`

**"Missing VITE_PINATA_JWT"**
- Generate JWT in Pinata dashboard
- Add to `.env` as `VITE_PINATA_JWT`
- Restart dev server

**Wallet Connection Fails**
- Pera Wallet: Ensure app/extension is installed and on correct network
- Local Wallet: Verify AlgoKit LocalNet is running (`algokit localnet status`)
- Check KMD environment variables

**Transaction Fails**
- Ensure wallet is connected
- Verify account has sufficient funds
- Check that contract is deployed and App ID is correct
- Verify batch is in correct state for the operation

**Build Errors**
- Clear node_modules: `rm -rf node_modules && npm install`
- Clear build cache: `rm -rf dist .vite`
- Verify Node.js version: `node -v` (should be 18+)

---

## AlgoKit Workspaces

This project supports AlgoKit workspaces for monorepo management. Use `algokit project run` commands for orchestration across multiple projects.

**Example Commands:**
```bash
# From workspace root
algokit project run build        # Build all projects
algokit project run frontend     # Run frontend dev server
algokit project run test         # Run all tests
```

---

## Resources

- **AlgoKit Documentation**: [https://github.com/algorandfoundation/algokit-cli](https://github.com/algorandfoundation/algokit-cli)
- **React Documentation**: [https://react.dev](https://react.dev)
- **Vite Documentation**: [https://vitejs.dev](https://vitejs.dev)
- **Tailwind CSS**: [https://tailwindcss.com](https://tailwindcss.com)
- **use-wallet Documentation**: [https://github.com/txnlab/use-wallet](https://github.com/txnlab/use-wallet)
- **Pera Wallet**: [https://perawallet.app](https://perawallet.app)
- **Pinata Documentation**: [https://docs.pinata.cloud](https://docs.pinata.cloud)

---

## Contributing

When contributing to this project:

1. Follow the existing code style
2. Run linting before committing: `npm run lint`
3. Add tests for new features
4. Update documentation as needed
5. Ensure all tests pass: `npm test`

---

## License

This project is based on the AlgoKit template and follows the same licensing terms.
