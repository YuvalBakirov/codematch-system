<template>
  <div class="code-input">
    <div class="title-image">
      <img src="/images/codeMatch-logo.png" width="350" alt="codeMatch Logo" />
    </div>

    <!-- Important Note -->
    <div class="important-note">
      <p><strong><i class="fas fa-exclamation-circle small-icon"></i> Important Note </strong><br />
        For the best results, please insert a code snippet that represents a single functionality.
        <br />
        <em><i class="fas fa-star small-icon"></i> Preferably <b>ONE</b> class or function.</em></p>
    </div>

    <textarea 
      v-model="code" 
      placeholder="Enter code snippet..." 
      :maxlength="maxChars"
    ></textarea>

    <!-- Display the model name under the textarea -->
    <div class="model-name">
      <p><strong>Model in Use:</strong> {{ modelName }}</p>
    </div>

    <!-- Submit button -->
    <button @click="submitCode">
      <div v-if="loading" class="loading-spinner"></div>
      Submit
    </button>
  </div>
</template>

<script>
import axios from 'axios';


export default {
  data() {
    return {
      code: this.$route.query.code || "",
      minWords: 50,  // Constant for minimum word count
      maxWords: 500,  // Constant for maximum word count
      loading: false, // New property for loading state
      modelName: "" // New variable for model name
    };
  },
  computed: {

  },
  mounted() {
    this.fetchModelName(); // Fetch the model name when the component is mounted
  },
  watch: {
    "$route.query.code"(newCode) {
      if (newCode) {
        this.code = newCode;
      }
    }
  },
  methods: {
    async fetchModelName() {
      try {
        const backendUrl =
          process.env.NODE_ENV === "production"
            ? "http://backend:8000" // Docker-internal hostname for production
            : "http://localhost:8000"; // Localhost for development

        const response = await axios.get(`${backendUrl}/get_model_name`);
        this.modelName = response.data.model_name;
      } catch (error) {
        console.error("Error fetching model name:", error);
        this.modelName = "Error fetching model name!";
      }
    },
    async submitCode() {
      this.loading = true; // Start loading

      try {
        // Send the code to the FastAPI backend

        const backendUrl =
          process.env.NODE_ENV === "production"
            ? "http://backend:8000" // Docker-internal hostname for production
            : "http://localhost:8000"; // Localhost for development


        // const response = await axios.post("http://localhost:8000/process_code", { code: this.code });
        // const response = await axios.post("http://backend:8000/process_code", { code: this.code });
        const response = await axios.post(`${backendUrl}/process_code`, { code: this.code });
        const results = response.data; // Get the results from the response
        console.log("Received results from backend:", results); // Log the response data

        
        // Navigate to the Results page and pass the code and results as query parameters
        this.$router.push({ 
          path: "/results", 
          query: { code: this.code, results: JSON.stringify(results)}
        });
      } catch (error) {
        console.error("Error sending code to backend:", error);
        alert("Failed to send the code to the backend. Check the console for details.");
      } finally {
      this.loading = false; // Stop loading after request completes
    }
    }
  }
};
</script>


<style scoped>
.code-input {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.important-note {
  text-align: left;
  width: 50%;
  background-color: #fffbeb;
  border: 1px solid #ffdf91;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Adds a soft shadow */
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(-5px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

textarea {
  width: 50%;
  height: 300px;
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  font-family: 'Roboto Mono', monospace;
  transition: border-color 0.3s ease;
  resize: vertical; /* Allow vertical resizing */
}

.model-name {
  text-align: left;
  width: 50%; /* Match the textarea width */
  margin-top: 5px; /* Add a small space between textarea and text */
}

button {
  margin-top: 20px; /* Add spacing between the button and model-name */
  padding: 10px 20px;
  font-size: 16px;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #333;
}

h1 {
  font-size: 2rem;
  margin-bottom: 20px;
  color: #333;

}

.small-icon {
  font-size: 0.7rem; /* Adjust the size as needed */
  vertical-align: middle; /* Aligns icon vertically with text */
}

.loading-spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top: 4px solid #007bff;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  animation: spin 1s linear infinite;
  margin-left: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>

