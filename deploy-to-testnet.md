# Deploy FoodSafety Contract to TestNet

## Option 1: Deploy via Web App (Recommended)

1. Deploy frontend to Vercel
2. Open the deployed app
3. Connect Pera Wallet (make sure you have TestNet ALGO)
4. Click "Deploy" button in the app
5. Save the App ID that appears

## Option 2: Deploy via AlgoKit CLI

### Step 1: Get TestNet ALGO
1. Go to https://bank.testnet.algorand.network/
2. Enter your Pera Wallet address
3. Get 10 ALGO

### Step 2: Set up deployer account
```bash
cd Hackseries-2-QuickStart-template/projects/contracts

# Export your Pera Wallet mnemonic (25 words)
# WARNING: Keep this secret! Never commit to git!
export DEPLOYER_MNEMONIC="your 25 word mnemonic phrase here"

# Deploy
algokit project deploy testnet
```

### Step 3: Save the App ID
After deployment, you'll see output like:
```
FoodSafety deployed. App ID: 123456789
```

Save that App ID - you'll need it to interact with the contract!

## Where to Use the App ID

The App ID is NOT an environment variable. Users enter it directly in the web app:
1. Open your deployed app
2. In the "Deploy Contract" section, there's an input field
3. Enter your App ID there
4. Now you can create batches, inspect, distribute, etc.

## Important Notes

- Each deployment creates a NEW App ID
- You can reuse the same App ID across sessions
- Share the App ID with other users so they can interact with your contract
- You can view your contract on TestNet explorer: https://testnet.explorer.perawallet.app/application/YOUR_APP_ID
