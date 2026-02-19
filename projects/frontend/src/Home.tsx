// src/components/Home.tsx
import { useWallet } from '@txnlab/use-wallet-react'
import React, { useState } from 'react'
import ConnectWallet from './components/ConnectWallet'
import FoodSafety from './components/FoodSafety'

interface HomeProps {}

const Home: React.FC<HomeProps> = () => {
  const [openWalletModal, setOpenWalletModal] = useState<boolean>(false)
  const [foodSafetyModal, setFoodSafetyModal] = useState<boolean>(false)
  const { activeAddress } = useWallet()

  const toggleWalletModal = () => {
    setOpenWalletModal(!openWalletModal)
  }

  return (
    <div className="min-h-screen bg-gradient-to-tr from-teal-400 via-cyan-300 to-sky-400 relative">
      {/* Top-right wallet connect button */}
      <div className="absolute top-4 right-4 z-10">
        <button
          data-test-id="connect-wallet"
          className="btn btn-accent px-5 py-2 text-sm font-medium rounded-full shadow-md"
          onClick={toggleWalletModal}
        >
          {activeAddress ? 'Wallet Connected' : 'Connect Wallet'}
        </button>
      </div>

      {/* Centered content with background blur for readability */}
      <div className="flex items-center justify-center min-h-screen px-4">
        <div className="backdrop-blur-md bg-white/70 rounded-2xl p-8 shadow-xl max-w-5xl w-full">
          <h1 className="text-4xl font-extrabold text-teal-700 mb-6 text-center">AgriTrust - Food Safety & Traceability</h1>
          <p className="text-gray-700 mb-8 text-center">Blockchain-based food safety system built on Algorand</p>

          <div className="grid grid-cols-1 gap-6">
            <div className="card bg-gradient-to-br from-green-600 to-emerald-600 text-white shadow-xl">
              <div className="card-body">
                <h2 className="card-title">AgriTrust - Food Safety</h2>
                <p>Create batches, inspect, distribute, and recall food products with blockchain traceability.</p>
                <div className="card-actions justify-end">
                  <button className="btn btn-outline" disabled={!activeAddress} onClick={() => setFoodSafetyModal(true)}>Open</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <ConnectWallet openModal={openWalletModal} closeModal={toggleWalletModal} />
      <FoodSafety openModal={foodSafetyModal} closeModal={() => setFoodSafetyModal(false)} />
    </div>
  )
}

export default Home
