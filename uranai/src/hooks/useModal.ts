"use client";

import { useState, useCallback } from 'react';

export type ModalType = 'login' | 'register' | 'premium' | 'ticket' | 'addPerson' | 'confirmPerson';

export function useModal() {
  const [activeModal, setActiveModal] = useState<ModalType | null>(null);
  const [modalData, setModalData] = useState<any>(null);

  const openModal = useCallback((type: ModalType, data?: any) => {
    setActiveModal(type);
    if (data) setModalData(data);
  }, []);

  const closeModal = useCallback(() => {
    setActiveModal(null);
    setModalData(null);
  }, []);

  return {
    activeModal,
    modalData,
    openModal,
    closeModal,
  };
}
