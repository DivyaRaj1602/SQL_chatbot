class ChatHistory:
    def __init__(self):
        self.history = []
        self.last_result = None
        self.last_analyzer = None

    def add(self, user_input, result):
        """Add a user query and its result to history"""
        self.history.append({
            "user_input": user_input,
            "result": result,
            "timestamp": self._get_timestamp()
        })
        self.last_result = result

    def add_analyzer(self, analyzer):
        """Store the last data analyzer for reuse"""
        self.last_analyzer = analyzer

    def get_last_result(self):
        """Get the most recent query result"""
        return self.last_result

    def get_last_analyzer(self):
        """Get the most recent data analyzer"""
        return self.last_analyzer

    def get(self):
        """Get full chat history"""
        return self.history

    def clear(self):
        """Clear all history"""
        self.history = []
        self.last_result = None
        self.last_analyzer = None

    def show_history(self):
        """Display chat history in a nice format"""
        if not self.history:
            print("📚 No chat history yet.")
            return
        
        print("\n📚 Chat History:")
        print("=" * 60)
        
        for i, entry in enumerate(self.history, 1):
            print(f"\n{i}. Query: {entry['user_input']}")
            print(f"   Time: {entry['timestamp']}")
            if entry['result']['success']:
                print(f"   ✅ Found {entry['result']['result_count']} rows")
            else:
                print(f"   ❌ Failed: {entry['result']['error']}")
        
        print("=" * 60)

    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def has_recent_data(self):
        """Check if there's recent data available for analysis"""
        return (self.last_result is not None and 
                self.last_result['success'] and 
                self.last_result['results'] and
                self.last_analyzer is not None)