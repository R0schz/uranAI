let tickets = 5;

export const getTicketCount = (): number => {
  return tickets;
};

export const useTicket = (): boolean => {
  if (tickets > 0) {
    tickets--;
    console.log('Ticket used. Remaining tickets:', tickets);
    return true;
  } else {
    console.log('No tickets available.');
    return false;
  }
};

export const replenishTickets = (amount: number): void => {
  tickets += amount;
  console.log('Tickets replenished. Total tickets:', tickets);
};
