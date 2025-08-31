"use client";

import { useAppContext, ModalType } from '../../contexts/AppContext';
import LoginModal from './LoginModal';
import RegisterModal from './RegisterModal';
import PremiumModal from './PremiumModal';
import TicketModal from './TicketModal';
import AddPersonModal from './AddPersonModal';
import ConfirmPersonModal from './ConfirmPersonModal';

interface ModalContainerProps {
  activeModal: ModalType;
}

const ModalContainer: React.FC<ModalContainerProps> = ({ activeModal }) => {
  if (!activeModal) return null;

  const renderModal = () => {
    switch (activeModal) {
      case 'login':
        return <LoginModal />;
      case 'register':
        return <RegisterModal />;
      case 'premium':
        return <PremiumModal />;
      case 'ticket':
        return <TicketModal />;
      case 'addPerson':
        return <AddPersonModal />;
      case 'confirmPerson':
        return <ConfirmPersonModal />;
      default:
        return null;
    }
  };

  return (
    <div id="modal-container" className="fixed inset-0 z-50">
      {renderModal()}
    </div>
  );
};

export default ModalContainer;
