interface Person {
  id: number;
  nickname: string;
  name: string;
  gender: string;
  birthDate: string;
  birthTime: string;
  birthPlace: string;
}

let people: Person[] = [
  {
    id: 1,
    nickname: 'あなた',
    name: 'てすと はなこ',
    gender: 'female',
    birthDate: '1998-11-10',
    birthTime: '14:30',
    birthPlace: '東京都渋谷区',
  },
];

export const addPerson = (person: Person): void => {
  people.push(person);
  console.log('Person added:', person);
};

export const updatePerson = (id: number, updatedPerson: Partial<Person>): void => {
  const index = people.findIndex((p) => p.id === id);
  if (index !== -1) {
    people[index] = { ...people[index], ...updatedPerson };
    console.log('Person updated:', people[index]);
  }
};

export const deletePerson = (id: number): void => {
  people = people.filter((p) => p.id !== id);
  console.log('Person deleted with id:', id);
};

export const getPeople = (): Person[] => {
  return people;
};
