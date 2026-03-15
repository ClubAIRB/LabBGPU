import { create } from 'zustand';
import { Head, Organization } from '../services/apiServices';

interface AuthState {
  user: Head | null;
  isAuthenticated: boolean;
  token: string | null;
  login: (token: string, user: Head) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  token: null,
  
  login: (token: string, user: Head) => {
    localStorage.setItem('access_token', token);
    set({ 
      token, 
      user, 
      isAuthenticated: true 
    });
  },
  
  logout: () => {
    localStorage.removeItem('access_token');
    set({ 
      token: null, 
      user: null, 
      isAuthenticated: false 
    });
  },
}));

interface OrganizationState {
  organizations: Organization[];
  currentOrganization: Organization | null;
  setOrganizations: (orgs: Organization[]) => void;
  setCurrentOrganization: (org: Organization | null) => void;
}

export const useOrganizationStore = create<OrganizationState>((set) => ({
  organizations: [],
  currentOrganization: null,
  
  setOrganizations: (orgs: Organization[]) => {
    set({ organizations: orgs });
  },
  
  setCurrentOrganization: (org: Organization | null) => {
    set({ currentOrganization: org });
  },
}));
