interface IUser {
  id: number;
  image: string;
  first_name: string;
  last_name: string;
  middle_name: string;
  gender: 'Male' | 'Female';
  phone: string;
  email: string;
  tg_acc: string;
  ya_programm: string;
  purpose: string;
  education: string;
  work: string;
  address: {
    country: string;
    city: string;
    street_home: string;
    post_index: number;
  };
  size: {
    clothes_size: 'XS' | 'S' | 'M' | 'L' | 'XL';
    foot_size: '35' | '36' | '37' | '38' | '39' | '40' | '41' | '42' | '43' | '44' | '45';
  };
  actions: [
    {
      title: string;
    }
  ];
  status: 'Active' | 'Clarify' | 'Pause' | 'Not active';
  achievement: 'new' | 'friend' | 'profi_friend';
  created: string;
}

interface IUserContent {
  id: number;
  image: string;
  first_name: string;
  last_name: string;
  middle_name: string;
  phone: string;
  email: string;
  tg_acc: string;
  ya_programm: string;
  city: string;
  my_content: IContent[];
  status: 'Active' | 'Clarify' | 'Pause' | 'Not active';
  achievement: 'new' | 'friend' | 'profi_friend';
  rating: number;
}

interface IContent {
  id: number;
  created_at: string;
  platform: 'habr' | 'VC' | 'youtube' | 'telegram' | 'instagram' | 'linkedin' | 'other';
  link: string;
  documents: number;
}

interface IData {
  x: string;
  habr?: IContent[];
  VC?: IContent[];
  youtube?: IContent[];
  telegram?: IContent[];
  instagram?: IContent[];
  linkedin?: IContent[];
  other?: IContent[];
}

export type { IUser, IUserContent, IContent, IData };
