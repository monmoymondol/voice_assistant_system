# voice_assistant_system
t’s a minimal, runnable scaffold that wires the main pieces together which can iterate quickly: backend APIs(chat+voice+face) a simple offline chatbot module, integrations hooks, dense KB retriever stub, a Python voice client (VOSK optional) and a React voice UI scaffold. Each file is a  model internals, retriever models, and integration endpoints 

### Voice Assistant Project File Structure
Below is a complete, organized file structure for a local Voice Assistant that integrates with your offline chatbot, web UI, face recognition, e‑commerce, invoice, and knowledge modules. It includes both web and standalone Python voice clients, offline STT (VOSK) support, TTS, wake‑word hooks, and integration hooks.

voice_assistant_system/                                                                                                                       
├── backend/                                                                                                                                  
│   ├── app.py                                                                                                                                
│   ├── api/                                                                                                                                  
│   │   ├── chat_api.py                                                                                                                       
│   │   ├── voice_api.py                                                                                                                      
│   │   └── face_api.py                                                                                                                       
│   ├── chatbot/                                                                                                                              
│   │   ├── chatbot.py                                                                                                                        
│   │   ├── memory.py                                                                                                                         
│   │   ├── persona.py                                                                                                                        
│   │   ├── model.py                                                                                                                          
│   │   ├── tokenizer.py                                                                                                                      
│   │   └── generate.py                                                                                                                       
│   ├── integrations/                                                                                                                        
│   │   ├── integrations.py                                                                                                                  
│   │   └── ecommerce_client.py                                                                                                              
│   ├── kb/                                                                                                                                  
│   │   ├── kb_index_dense.py                                                                                                                
│   │   └── retriever_faiss.py                                                                                                                
│   ├── resume_analyzer/                                                                                                                      
│   │   ├── parser.py                                                                                                                         
│   │   └── analyzer.py                                                                                                                       
│   └── requirements.txt                                                                                                                      
│                                                                                                                                            
├── voice_clients/                                                                                                                            
│   ├── python_assistant/                                                                                                                     
│   │   ├── voice_assistant.py                                                                                                                
│   │   ├── stt_vosk.py                                                                                                                      
│   │   ├── tts_pyttsx3.py                                                                                                                    
│   │   ├── wakeword_porcupine.py    # optional                                                                                               
│   │   └── requirements.txt                                                                                                                  
│   └── web_assistant/                                                                                                                        
│       ├── react-voice-ui/                                                                                                                  
│       │   ├── package.json                                                                                                                  
│       │   ├── public/                                                                                                                      
│       │   │   └── index.html                                                                                                                
│       │   └── src/                                                                                                                          
│       │       ├── index.js                                                                                                                  
│       │       ├── App.js                                                                                                                    
│       │       ├── components/                                                                                                               
│       │       │   ├── VoiceAssistant.js                                                                                                     
│       │       │   └── WebcamStream.js
│       │       └── styles.css                                                                                                                
│       └── README.md                                                                                                                         
│                                                                                                                                             
├── face_recognition/                                                                                                                         
│   ├── utils/                                                                                                                              
│   │   ├── detector.py                                                                                                                      
│   │   ├── embedder.py                                                                                                                       
│   │   └── datastore.py                                                                                                                      
│   ├── scripts/                                                                                                                              
│   │   ├── build_embeddings.py                                                                                                              
│   │   ├── enroll.py                                                                                                                         
│   │   └── recognize.py                                                                                                                      
│   └── requirements.txt                                                                                                                      
│                                                                                                                                             
├── web_ui/                                                                                                                                   
│   ├── web_ui.py                                                                                                                            
│   └── templates/                                                                                                                            
│       └── index.html                                                                                                                        
│                                                                                                                                             
├── docs/                                                                                                                                    
│   ├── architecture.md                                                                                                                       
│   ├── run_instructions.md                                                                                                                   
│   └── api_spec.md                                                                                                                          
│                                                                                                                                            
└── tools/                                                                                                                                    
    ├── setup_env.sh                                                                                                                          
    └── build_kb_index.sh                                                                                                                    
                                                                                                                                            
How to use: copy each file into the matching path in your project tree, install the listed requirements, then run the backend and clients per the run_instructions section at the end.

Quick start (local, minimal)
Create folders matching the structure and save the files above in the indicated paths.

Install dependencies (use the setup_env.sh script or install manually).

bash
cd voice_assistant_system
bash tools/setup_env.sh
source .venv/bin/activate
Start backend

bash
python backend/app.py
Backend runs at http://localhost:8000/.

Download a VOSK model (if you want offline STT) and set VOSK_MODEL_PATH or place it at voice_clients/python_assistant/models/vosk-model-small-en-us-0.15. Example models: https://alphacephei.com/vosk/models

Run the Python voice assistant

bash
Say the wake word hey assistant and then speak a command.

Web voice client (optional) — point the React VoiceAssistant to http://localhost:8000/api/voice/ and use the browser Web Speech API.

