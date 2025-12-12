class AIContentGenerator {
    constructor(containerId, onContentGenerated) {
        this.container = document.getElementById(containerId);
        this.onContentGenerated = onContentGenerated;
        this.init();
    }

    init() {
        this.render();
        this.setupEventListeners();
    }

    render() {
        this.container.innerHTML = `
            <div class="ai-generator-container">
                <h3>AI Content Generator</h3>
                <p class="subtitle">Create and assign educational content powered by AI.</p>
                
                <div class="form-group">
                    <label for="contentType">Content Type</label>
                    <select id="contentType" class="form-control">
                        <option value="quiz">Quiz Questions</option>
                        <option value="summary">Summary</option>
                        <option value="flashcards">Flashcards</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="topic">Topic</label>
                    <input type="text" id="topic" class="form-control" 
                           placeholder="Enter topic (e.g., 'Photosynthesis', 'World War II')" required>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="difficulty">Difficulty Level</label>
                        <select id="difficulty" class="form-control">
                            <option value="beginner">Beginner</option>
                            <option value="intermediate" selected>Intermediate</option>
                            <option value="advanced">Advanced</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="numQuestions">Number of Questions</label>
                        <input type="number" id="numQuestions" class="form-control" min="1" max="20" value="5">
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="customInstructions">Custom Instructions</label>
                    <textarea id="customInstructions" class="form-control" rows="3"
                              placeholder="e.g., 'Focus on multiple choice questions', 'Include diagrams'"></textarea>
                </div>
                
                <div class="form-actions">
                    <button type="button" id="generateContentBtn" class="btn btn-primary">
                        <i class="fas fa-magic"></i> Generate Content
                    </button>
                    <button type="button" id="resetGeneratorBtn" class="btn btn-outline-secondary">
                        <i class="fas fa-undo"></i> Reset
                    </button>
                </div>
                
                <div id="generatorStatus" class="status-message"></div>
                
                <div id="generatedContent" class="generated-content" style="display: none;">
                    <h4>Generated Content</h4>
                    <div id="contentPreview" class="content-preview"></div>
                    <div class="content-actions">
                        <button type="button" id="useContentBtn" class="btn btn-success">
                            <i class="fas fa-check"></i> Use This Content
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    
    setupEventListeners() {
        document.getElementById('generateContentBtn').addEventListener('click', () => this.generateContent());
        document.getElementById('resetGeneratorBtn').addEventListener('click', () => this.resetGenerator());
        document.getElementById('useContentBtn').addEventListener('click', () => this.useGeneratedContent());
    }
    
    async generateContent() {
        const contentType = document.getElementById('contentType').value;
        const topic = document.getElementById('topic').value.trim();
        const difficulty = document.getElementById('difficulty').value;
        const numQuestions = document.getElementById('numQuestions').value;
        const customInstructions = document.getElementById('customInstructions').value;
        
        if (!topic) {
            this.showStatus('Please enter a topic', 'error');
            return;
        }
        
        this.showStatus('Generating content...', 'info');
        
        try {
            // Call your backend API to generate content
            const response = await fetch('/api/ai/generate-content', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: JSON.stringify({
                    content_type: contentType,
                    topic,
                    difficulty,
                    num_questions: numQuestions,
                    instructions: customInstructions
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to generate content');
            }
            
            const data = await response.json();
            this.displayGeneratedContent(data.content);
            this.generatedData = data;
            this.showStatus('Content generated successfully!', 'success');
            
        } catch (error) {
            console.error('Error generating content:', error);
            this.showStatus('Failed to generate content. Please try again.', 'error');
        }
    }
    
    displayGeneratedContent(content) {
        const preview = document.getElementById('contentPreview');
        preview.innerHTML = ''; // Clear previous content
        
        if (Array.isArray(content)) {
            // For quiz questions
            const questionsList = document.createElement('div');
            questionsList.className = 'questions-list';
            
            content.forEach((question, index) => {
                const questionEl = document.createElement('div');
                questionEl.className = 'question-item';
                questionEl.innerHTML = `
                    <div class="question-text"><strong>${index + 1}.</strong> ${question.question}</div>
                    <div class="options">
                        ${question.options ? question.options.map((opt, i) => 
                            `<div class="option ${i === question.correctAnswer ? 'correct' : ''}">
                                ${String.fromCharCode(65 + i)}. ${opt}
                            </div>`
                        ).join('') : ''}
                    </div>
                    ${question.explanation ? 
                        `<div class="explanation"><strong>Explanation:</strong> ${question.explanation}</div>` : ''}
                `;
                questionsList.appendChild(questionEl);
            });
            
            preview.appendChild(questionsList);
        } else {
            // For other content types
            preview.textContent = content;
        }
        
        document.getElementById('generatedContent').style.display = 'block';
    }
    
    useGeneratedContent() {
        if (this.generatedData && this.onContentGenerated) {
            this.onContentGenerated(this.generatedData);
            this.container.innerHTML = ''; // Close the generator
        }
    }
    
    resetGenerator() {
        document.getElementById('topic').value = '';
        document.getElementById('customInstructions').value = '';
        document.getElementById('generatedContent').style.display = 'none';
        this.showStatus('', 'info');
    }
    
    showStatus(message, type = 'info') {
        const statusEl = document.getElementById('generatorStatus');
        if (!statusEl) return;
        
        statusEl.textContent = message;
        statusEl.className = `status-message ${type}`;
        
        if (!message) {
            statusEl.style.display = 'none';
        } else {
            statusEl.style.display = 'block';
        }
    }
}

class TeacherAssignmentForm {
    constructor(containerId, onAssignmentCreated) {
        this.container = document.getElementById(containerId);
        this.onAssignmentCreated = onAssignmentCreated;
        this.classes = [];
        this.concepts = [];
        this.init();
    }

    async init() {
        await this.loadClasses();
        await this.loadConcepts();
        this.render();
        this.setupEventListeners();
    }

    async loadClasses() {
        try {
            const token = localStorage.getItem('access_token');
            if (!token) {
                throw new Error('No authentication token found');
            }
            
            const response = await fetch('/api/teacher/classes', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || 'Failed to load classes');
            }
            
            this.classes = await response.json();
        } catch (error) {
            console.error('Error loading classes:', error);
            this.showError(error.message || 'Failed to load classes. Please try again.');
        }
    }

    async loadConcepts() {
        try {
            const token = localStorage.getItem('access_token');
            if (!token) {
                throw new Error('No authentication token found');
            }
            
            const response = await fetch('/api/concepts', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || 'Failed to load concepts');
            }
            
            this.concepts = await response.json();
        } catch (error) {
            console.error('Error loading concepts:', error);
            this.showError(error.message || 'Failed to load concepts. Please try again.');
        }
    }

    render() {
        this.container.innerHTML = `
            <div class="ai-generator-toggle">
                <button id="toggleAIGenerator" class="btn btn-outline-primary">
                    <i class="fas fa-magic"></i> AI Content Generator
                </button>
            </div>
            
            <div id="aiGeneratorContainer" style="display: none; margin-bottom: 2rem;"></div>
            <div class="assignment-form-container">
                <h2>Create New Assignment</h2>
                <form id="assignmentForm">
                    <div class="form-group">
                        <label for="title">Title</label>
                        <input type="text" id="title" name="title" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="description">Description</label>
                        <textarea id="description" name="description" rows="3" required></textarea>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="concept">Concept</label>
                            <select id="concept" name="concept_id" required>
                                <option value="">Select Concept</option>
                                ${this.concepts.map(concept => 
                                    `<option value="${concept.id}">${concept.name}</option>`
                                ).join('')}
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="difficulty">Difficulty Level</label>
                            <select id="difficulty" name="difficulty_level" required>
                                <option value="1">Very Easy</option>
                                <option value="2">Easy</option>
                                <option value="3" selected>Medium</option>
                                <option value="4">Hard</option>
                                <option value="5">Very Hard</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="contentUrl">Content URL (Optional)</label>
                        <input type="url" id="contentUrl" name="content_url">
                    </div>
                    
                    <div class="form-group">
                        <label for="classes">Assign to Classes</label>
                        <div class="class-selection">
                            ${this.classes.map(cls => `
                                <div class="checkbox-group">
                                    <input type="checkbox" id="class-${cls.id}" name="class_ids" value="${cls.id}">
                                    <label for="class-${cls.id}">${cls.name}</label>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="dueDate">Due Date</label>
                            <input type="datetime-local" id="dueDate" name="due_date" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="maxScore">Maximum Score</label>
                            <input type="number" id="maxScore" name="max_score" min="1" value="100" required>
                        </div>
                    </div>
                    
                    <div class="form-actions">
                        <button type="submit" class="btn btn-primary">Create Assignment</button>
                        <button type="button" id="cancelBtn" class="btn btn-secondary">Cancel</button>
                    </div>
                </form>
                
                <div id="errorMessage" class="error-message"></div>
            </div>
        `;
        
        // Set default due date to tomorrow at 5 PM
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        tomorrow.setHours(17, 0, 0, 0);
        document.getElementById('dueDate').value = tomorrow.toISOString().slice(0, 16);
    }
    
    setupEventListeners() {
        document.getElementById('assignmentForm').addEventListener('submit', this.handleSubmit.bind(this));
        document.getElementById('cancelBtn').addEventListener('click', () => this.container.innerHTML = '');
        
        // Toggle AI Generator
        const toggleBtn = document.getElementById('toggleAIGenerator');
        const aiContainer = document.getElementById('aiGeneratorContainer');
        
        if (toggleBtn && aiContainer) {
            toggleBtn.addEventListener('click', () => {
                const isVisible = aiContainer.style.display !== 'none';
                aiContainer.style.display = isVisible ? 'none' : 'block';
                toggleBtn.innerHTML = `<i class="fas fa-${isVisible ? 'magic' : 'times'}"></i> ${isVisible ? 'AI Content Generator' : 'Close Generator'}`;
                
                if (!isVisible && !this.aiGenerator) {
                    this.aiGenerator = new AIContentGenerator('aiGeneratorContainer', (content) => {
                        // When content is generated and user clicks "Use This Content"
                        this.applyGeneratedContent(content);
                    });
                }
            });
        }
    }
    
    async handleSubmit(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const data = {
            title: formData.get('title'),
            description: formData.get('description'),
            concept_id: parseInt(formData.get('concept_id')),
            difficulty_level: parseInt(formData.get('difficulty_level')),
            content_url: formData.get('content_url') || null,
            class_ids: Array.from(document.querySelectorAll('input[name="class_ids"]:checked')).map(cb => parseInt(cb.value)),
            due_date: formData.get('due_date'),
            max_score: parseInt(formData.get('max_score'))
        };
        
        try {
            const response = await fetch('/api/teacher/assignments', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to create assignment');
            }
            
            const result = await response.json();
            this.showSuccess('Assignment created successfully!');
            if (this.onAssignmentCreated) {
                this.onAssignmentCreated(result);
            }
            this.container.innerHTML = '';
            
        } catch (error) {
            console.error('Error creating assignment:', error);
            this.showError(error.message || 'Failed to create assignment');
        }
    }
    
    applyGeneratedContent(contentData) {
        // Apply the generated content to the form
        if (contentData.content_type === 'quiz') {
            const title = `Quiz: ${contentData.topic}`;
            let description = `AI-Generated Quiz on ${contentData.topic}\n\n`;
            
            // Format the quiz questions and answers
            contentData.content.forEach((q, i) => {
                description += `${i + 1}. ${q.question}\n`;
                if (q.options) {
                    q.options.forEach((opt, j) => {
                        description += `   ${String.fromCharCode(65 + j)}. ${opt}${j === q.correctAnswer ? ' (Correct)' : ''}\n`;
                    });
                }
                if (q.explanation) {
                    description += `   Explanation: ${q.explanation}\n\n`;
                }
            });
            
            // Update the form fields
            document.getElementById('title').value = title;
            document.getElementById('description').value = description;
            document.getElementById('difficulty').value = contentData.difficulty_level || '3';
            
            // Hide the generator
            document.getElementById('aiGeneratorContainer').style.display = 'none';
            document.getElementById('toggleAIGenerator').innerHTML = '<i class="fas fa-magic"></i> AI Content Generator';
        }
    }
    
    showError(message) {
        const errorElement = document.getElementById('errorMessage');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
            
            // Hide error after 5 seconds
            setTimeout(() => {
                errorElement.style.display = 'none';
            }, 5000);
        }
    }
    
    showSuccess(message) {
        // You can implement a success notification here
        alert(message);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TeacherAssignmentForm;
}
