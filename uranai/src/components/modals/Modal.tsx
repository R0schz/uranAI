"use client";

import React from 'react';

interface ModalProps {
  children: React.ReactNode;
  onClose: () => void;
  className?: string;
}

const Modal: React.FC<ModalProps> = ({ children, onClose, className = '' }) => {
  const handleOverlayClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
      onClick={handleOverlayClick}
    >
      <div className={`bg-gray-900 border border-gray-700 rounded-2xl w-full max-w-sm mx-auto p-8 relative ${className}`}>
        {children}
      </div>
    </div>
  );
};

export default Modal;