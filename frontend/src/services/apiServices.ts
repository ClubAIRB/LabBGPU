import apiClient from './api';

export interface Organization {
  id: number;
  inn: string;
  name: string | null;
  type: 'school' | 'kindergarten' | 'additional_education';
  region: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface Head {
  id: number;
  full_name: string | null;
  organization_id: number | null;
  organization?: Organization;
  last_test_date: string | null;
  last_results: Record<string, any> | null;
  is_candidate: boolean;
  created_at: string;
}

export interface TestSession {
  id: number;
  head_id: number;
  organization_id: number | null;
  test_date: string;
  answers: Record<string, any>;
  scores: Record<string, any> | null;
  case_answers: Record<string, any> | null;
}

export const authApi = {
  headLogin: async (inn: string) => {
    const response = await apiClient.post('/auth/head/login', { inn });
    return response.data;
  },
  
  getCurrentHead: async () => {
    const response = await apiClient.get('/heads/me');
    return response.data;
  },
  
  updateHeadProfile: async (data: { full_name?: string }) => {
    const response = await apiClient.put('/heads/me', data);
    return response.data;
  },
};

export const organizationApi = {
  uploadExcel: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post('/organizations/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
  
  listOrganizations: async (params?: { skip?: number; limit?: number; org_type?: string }) => {
    const response = await apiClient.get('/organizations/', { params });
    return response.data;
  },
  
  getOrganization: async (orgId: number) => {
    const response = await apiClient.get(`/organizations/${orgId}`);
    return response.data;
  },
};

export const headApi = {
  getProfile: async () => {
    const response = await apiClient.get('/heads/me');
    return response.data;
  },
  
  updateProfile: async (data: { full_name?: string }) => {
    const response = await apiClient.put('/heads/me', data);
    return response.data;
  },
  
  createTestSession: async (data: { 
    answers: Record<string, any>; 
    scores?: Record<string, any>;
    case_answers?: Record<string, any>;
  }) => {
    const response = await apiClient.post('/heads/sessions', data);
    return response.data;
  },
  
  getTestSessions: async (params?: { skip?: number; limit?: number }) => {
    const response = await apiClient.get('/heads/sessions', { params });
    return response.data;
  },
};
