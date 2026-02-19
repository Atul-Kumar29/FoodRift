# AgriTrust - Blockchain Food Safety and Traceability System

AgriTrust is a blockchain-based food safety and traceability system built on Algorand. It enables transparent tracking of food products through the supply chain, from production to distribution, with immutable records and cryptographic verification.

## Features

- **Food Safety Management**: Track batches through creation, inspection, distribution, and recall
- **IPFS Integration**: Store inspection documents and batch information off-chain with on-chain verification
- **Smart Contract Operations**: Manage batch lifecycle with state transitions and role-based access
- **Flexible Wallet Support**: Connect using Pera Wallet or Local Wallet (KMD)

---

## Project Setup

### Prerequisites

- Docker (running)
- Node.js 18+ and npm
- AlgoKit installed (see [official docs](https://github.com/algorandfoundation/algokit-cli#install))

### Installation

Clone the repository:

```bash
git clone https://github.com/marotipatre/Hackseries-2-QuickStart-template.git
cd Hackseries-2-QuickStart-template
```

Bootstrap the workspace (installs dependencies, sets up virtual environment):

```bash
algokit project bootstrap all
```

Build all projects:

```bash
algokit project run build
```

Run the frontend:

```bash
cd projects/frontend
npm install
npm run dev
```

---

## Environment Configuration

### Frontend Environment Variables

Create `projects/frontend/.env` with the following values:

```bash
# Network (Algod)
VITE_ALGOD_SERVER=https://testnet-api.algonode.cloud
VITE_ALGOD_PORT=
VITE_ALGOD_TOKEN=
VITE_ALGOD_NETWORK=testnet

# Indexer (for batch queries)
VITE_INDEXER_SERVER=https://testnet-idx.algonode.cloud
VITE_INDEXER_PORT=
VITE_INDEXER_TOKEN=

# Optional: KMD (if using Local Wallet for development)
VITE_KMD_SERVER=http://localhost
VITE_KMD_PORT=4002
VITE_KMD_TOKEN=a-super-secret-token
VITE_KMD_WALLET=unencrypted-default-wallet
VITE_KMD_PASSWORD=some-password

# Pinata (IPFS integration for document storage)
# Generate a JWT in Pinata and paste below
VITE_PINATA_JWT=eyJhbGciOi...  # JWT from Pinata
# Optional: custom gateway
VITE_PINATA_GATEWAY=https://gateway.pinata.cloud/ipfs
```

**Notes:**
- Algod/Indexer config is read by `src/utils/network/getAlgoClientConfigs.ts`
- Pinata integration expects `VITE_PINATA_JWT` for document uploads (see `src/utils/pinata.ts`)
- Restart the dev server after editing `.env`

### Pinata Setup for IPFS

1. Create a Pinata account at [https://app.pinata.cloud](https://app.pinata.cloud)
2. Generate an API Key/JWT: [https://app.pinata.cloud/developers/api-keys](https://app.pinata.cloud/developers/api-keys)
3. Add the JWT to `projects/frontend/.env` as `VITE_PINATA_JWT`
4. Restart the dev server

---

## Wallet Integration

AgriTrust supports two wallet providers for connecting to the Algorand blockchain:

### Pera Wallet

Pera Wallet is a mobile and web wallet for Algorand that provides a secure way to manage your assets and interact with dApps.

**Features:**
- Mobile app (iOS/Android) and browser extension
- QR code connection for mobile
- Secure transaction signing
- Multi-account support

**How to connect:**
1. Install Pera Wallet from [https://perawallet.app](https://perawallet.app)
2. Create or import an account
3. In AgriTrust, click "Connect Wallet"
4. Select "Pera Wallet"
5. Scan the QR code with your mobile app or approve in the browser extension

### Local Wallet (KMD)

Local Wallet uses Algorand's Key Management Daemon (KMD) for local development and testing.

**Features:**
- Best for development and testing
- Works with AlgoKit LocalNet
- No mobile app required
- Fast transaction signing

**How to connect:**
1. Ensure AlgoKit LocalNet is running: `algokit localnet start`
2. Configure KMD environment variables in `.env`
3. In AgriTrust, click "Connect Wallet"
4. Select "Local Wallet"
5. Choose an account from the list

### Wallet Provider Selection

The wallet connection modal displays both options with clear icons and descriptions. You can switch between wallets by disconnecting and reconnecting with a different provider.

---

## Food Safety Smart Contract

### FoodSafetyApp Contract

The core smart contract manages the complete lifecycle of food batches with role-based access control.

#### Batch Lifecycle States

```
CREATED (0) → APPROVED (2) or REJECTED (3)
APPROVED (2) → DISTRIBUTED (4)
Any State → RECALLED (5) [by creator only]
```

#### Smart Contract Operations

**Create Batch**
- Creates a new food batch with producer information, product details, and IPFS hash
- Initial status: CREATED
- Stores data in Box storage for efficiency

**Inspect Batch**
- Inspectors can approve or reject CREATED batches
- Stores inspection report IPFS hash
- Transitions to APPROVED or REJECTED state

**Distribute Batch**
- Distributors can mark APPROVED batches as distributed
- Transitions to DISTRIBUTED state
- Only works on APPROVED batches

**Recall Batch**
- Contract creator (regulator) can recall any batch
- Works from any state
- Transitions to RECALLED state

**Query Batch**
- Anyone can query batch information by batch ID
- Returns all stored data including status and IPFS hashes

---

## IPFS Integration

AgriTrust uses IPFS (via Pinata) for off-chain document storage with on-chain verification.

### Document Storage

**File Upload:**
- Upload inspection documents, certificates, photos
- Returns IPFS hash (CID) for on-chain storage
- Files are pinned to ensure availability

**JSON Upload:**
- Upload structured batch data as JSON
- Returns IPFS hash for metadata storage
- Useful for detailed product information

### Viewing Documents

IPFS links are displayed in the batch view interface. Click any IPFS hash to view the document via the configured gateway.

**Utilities:**
- `src/utils/pinata.ts` - Pinata integration functions
- `pinFileToIPFS(file)` - Upload file to IPFS
- `pinJSONToIPFS(json)` - Upload JSON to IPFS

---

## Project Structure

### Frontend

Location: `projects/frontend`

**Key Files:**
- `src/Home.tsx` - Landing page with food safety features
- `src/components/FoodSafety.tsx` - Main food safety operations component
- `src/components/ConnectWallet.tsx` - Wallet connection modal with provider selection
- `src/components/Account.tsx` - Display wallet information
- `src/utils/pinata.ts` - IPFS integration utilities
- `src/utils/network/getAlgoClientConfigs.ts` - Network configuration

### Smart Contracts

Location: `projects/contracts/smart_contracts`

**Structure:**
```
smart_contracts/
├── food_safety/
│   ├── contract.py          # FoodSafetyApp smart contract
│   └── deploy_config.py     # Deployment configuration
├── __init__.py
└── __main__.py
```

---

## Development Workflow

### Building Contracts

```bash
algokit project run build
```

### Deploying to LocalNet

```bash
algokit project deploy localnet
```

### Running Tests

**Smart Contract Tests:**
```bash
cd projects/contracts
pytest
```

**Frontend Tests:**
```bash
cd projects/frontend
npm test
```

### Running the Application

1. Start AlgoKit LocalNet (for local development):
```bash
algokit localnet start
```

2. Deploy contracts:
```bash
algokit project deploy localnet
```

3. Start the frontend:
```bash
cd projects/frontend
npm run dev
```

4. Open browser to `http://localhost:5173`

---

## Troubleshooting

### Missing Environment Variables

**Error:** "Missing VITE_ALGOD_SERVER"

**Solution:**
- Ensure `.env` exists in `projects/frontend`
- Verify all required variables are set
- Restart `npm run dev`

### IPFS Upload Failures

**Error:** "Missing VITE_PINATA_JWT" or upload fails

**Solution:**
- Generate JWT in Pinata dashboard
- Add to `.env` as `VITE_PINATA_JWT`
- Verify gateway URL is correct
- Restart dev server

### Wallet Connection Issues

**Pera Wallet:**
- Ensure Pera Wallet app/extension is installed
- Check that you're on the correct network (TestNet/MainNet)
- Try disconnecting and reconnecting

**Local Wallet:**
- Verify AlgoKit LocalNet is running: `algokit localnet status`
- Check KMD environment variables in `.env`
- Ensure KMD service is accessible

### Transaction Failures

**Common Issues:**
- Wallet not connected: Click "Connect Wallet" first
- Insufficient funds: Fund your account via [TestNet dispenser](https://bank.testnet.algorand.network/)
- Invalid App ID: Deploy the contract first or enter correct App ID
- State transition error: Verify batch is in correct state for the operation

---

## Continuous Integration / Continuous Deployment

### GitHub Actions

This project uses GitHub Actions for CI/CD workflows located in `.github/workflows`.

**Automated Checks:**
- Dependency installation
- Code linting (ESLint)
- Type checking
- Build verification
- Test execution

### Deployment

**Frontend Deployment:**

The project supports deployment to Netlify or Vercel. See `projects/frontend/README.md` for detailed deployment instructions.

**Smart Contract Deployment:**

Use `algokit project deploy` to deploy contracts to TestNet or MainNet:

```bash
algokit project deploy testnet
```

---

## Technology Stack

### Frontend
- **React** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **DaisyUI** - Component library for Tailwind
- **@txnlab/use-wallet-react** - Wallet integration
- **@perawallet/connect** - Pera Wallet provider
- **notistack** - Notification system

### Smart Contracts
- **Algorand Python** - Smart contract language
- **AlgoKit** - Development toolkit
- **PyTeal/Puya** - Python to TEAL compiler

### Storage
- **IPFS** - Decentralized file storage
- **Pinata** - IPFS pinning service
- **Box Storage** - Algorand on-chain storage

---

## Resources

- **Algorand Developer Portal**: [https://dev.algorand.co/](https://dev.algorand.co/)
- **AlgoKit Documentation**: [https://github.com/algorandfoundation/algokit-cli](https://github.com/algorandfoundation/algokit-cli)
- **AlgoKit Workshops**: [https://algorand.co/algokit-workshops](https://algorand.co/algokit-workshops)
- **Pera Wallet**: [https://perawallet.app](https://perawallet.app)
- **Pinata Documentation**: [https://docs.pinata.cloud](https://docs.pinata.cloud)
- **Algorand Developer YouTube**: [https://www.youtube.com/@algodevs](https://www.youtube.com/@algodevs)

---

## License

This project is based on the AlgoKit template and follows the same licensing terms.
