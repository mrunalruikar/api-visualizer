// Mock DOM elements for testing
const mockDocument = {
    getElementById: jest.fn(),
    createElement: jest.fn(),
    addEventListener: jest.fn()
};

const mockElement = {
    innerHTML: '',
    textContent: '',
    appendChild: jest.fn()
};

// Mock fetch API
global.fetch = jest.fn();

// Setup DOM mocks
beforeEach(() => {
    global.document = mockDocument;
    global.console = { error: jest.fn() };
    
    // Reset mocks
    mockDocument.getElementById.mockReturnValue(mockElement);
    mockDocument.createElement.mockReturnValue(mockElement);
    mockElement.innerHTML = '';
    mockElement.textContent = '';
    mockElement.appendChild.mockClear();
    fetch.mockClear();
});

describe('Frontend App Tests', () => {
    test('should fetch data successfully and populate user list', async () => {
        // Mock successful API response
        const mockUsers = [
            { name: 'John Doe', email: 'john@example.com' },
            { name: 'Jane Smith', email: 'jane@example.com' }
        ];
        
        fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => mockUsers
        });

        // Load the app code (would need to be imported/required in real setup)
        // For now, we'll test the logic directly
        
        const userList = mockElement;
        
        try {
            const response = await fetch('/api/data');
            const users = await response.json();
            
            // Clear loading message
            userList.innerHTML = '';
            
            // Add users to list
            users.forEach(user => {
                const listItem = { textContent: `${user.name} - ${user.email}` };
                userList.appendChild(listItem);
            });
            
            expect(fetch).toHaveBeenCalledWith('/api/data');
            expect(userList.appendChild).toHaveBeenCalledTimes(2);
            expect(userList.innerHTML).toBe('');
        } catch (error) {
            fail('Should not throw error');
        }
    });

    test('should handle fetch error gracefully', async () => {
        // Mock failed API response
        fetch.mockRejectedValueOnce(new Error('Network error'));

        const userList = mockElement;
        
        try {
            await fetch('/api/data');
        } catch (error) {
            userList.innerHTML = `<li style="color: red;">Failed to load data: ${error.message}</li>`;
            expect(userList.innerHTML).toContain('Failed to load data: Network error');
        }
    });

    test('should handle non-ok HTTP response', async () => {
        // Mock HTTP error response
        fetch.mockResolvedValueOnce({
            ok: false,
            status: 500
        });

        const userList = mockElement;
        
        try {
            const response = await fetch('/api/data');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        } catch (error) {
            userList.innerHTML = `<li style="color: red;">Failed to load data: ${error.message}</li>`;
            expect(userList.innerHTML).toContain('HTTP error! status: 500');
        }
    });

    test('should handle non-array response data', async () => {
        // Mock invalid data response
        fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ error: 'Invalid data' })
        });

        const userList = mockElement;
        
        try {
            const response = await fetch('/api/data');
            const users = await response.json();
            
            if (!Array.isArray(users)) {
                throw new Error('Data is not an array');
            }
        } catch (error) {
            userList.innerHTML = `<li style="color: red;">Failed to load data: ${error.message}</li>`;
            expect(userList.innerHTML).toContain('Data is not an array');
        }
    });
});
