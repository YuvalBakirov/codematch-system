<template>
  <div class="results" style="text-align: Center;">
    <div class="title-image">
      <img src="/images/codeMatch-logo.png" width="300" alt="codeMatch Logo" />
    </div>
    <p class="subtitle" style="font-size: 18px;" >View the most similar code snippets based on your input</p>
    <div class="content">
      
      <!-- Left Column: Code Display and Refresh Button -->
      <div class="code-display">
        
        <h3>The code you entered</h3>
        <textarea 
          v-model="code" 
          readonly 
          placeholder="The code you entered will appear here..."
        ></textarea>
        <button @click="refreshResults">Refresh</button>
      </div>

      <!-- Right Column: Sort Options and Results List -->
      <div class="result-list">
        <h3>Top Results</h3>
        
        <!-- Sorting Dropdown -->
        <label for="sortCriteria">Sort by:</label>
        <select id="sortCriteria" v-model="sortCriteria">
          <option value="airerank">AI Rerank (top 5 reviewed by Claude)</option>
          <option value="similarity">Similarity</option>
          <option value="language">Language</option>
          <option value="license">License</option>
          <option value="stars">Stars</option>
        </select>

        <ul>
          <li
            v-for="(result, index) in sortedResults"
            :key="index"
            :class="['result-item', { 'highlighted-result': parseFloat(result.similarity) === 1.00 }]"
          >
            <div class="result-header">
              <span class="result-number">{{ index + 1 }}.</span>
              <a :href="result.label" target="_blank">
                <img src="/images/github-icon.png" alt="GitHub logo" width="20" />
              </a>
              <!-- Replace the current label line with this in CodeResults.vue -->
              <a :href="result.label" target="_blank " class="label clickable-link">{{ result.label }}</a>
              <span v-if="result.reranked" class="rerank-badge" title="This candidate was independently reviewed and ranked by Claude, not just by embedding similarity">★ Reviewed by Claude</span>
            </div>
            <div class="result-details">
              <p>Language: <strong> {{ result.language }} </strong> |
              License: <strong>{{ result.licenses }} </strong> <i class="fas fa-file-contract small-icon"></i> |
              <!-- Display stars and icon only if stars exist -->
              <span v-if="result.stars !== 'No Stars'">Stars: <strong>{{ result.stars }} </strong>
                <img src="/images/github-star.png" alt="Stars" class="star-icon" />
              </span><span v-else><strong>No Stars</strong></span>
              </p>
              <p>Similarity: <span class="similarity-badge"><strong>  {{ (parseFloat(result.similarity) * 100).toFixed(2) }}% </strong></span></p>
            </div>
            
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      code: this.$route.query.code || "", // Retrieve the code from the query parameter
      results: JSON.parse(this.$route.query.results || "[]"), // Parse the results from the query parameter
      sortCriteria: "airerank"  // Default: show the AI-reranked order, not raw cosine similarity
    };
  },
  computed: {
    // Computed property to sort results based on selected criteria
    sortedResults() {
      return [...this.results].sort((a, b) => {
        if (this.sortCriteria === "airerank") {
          return (a.rerank_rank || 0) - (b.rerank_rank || 0);
        } else if (this.sortCriteria === "similarity") {
          return parseFloat(b.similarity) - parseFloat(a.similarity);
        } else if (this.sortCriteria === "language") {
          return a.language.localeCompare(b.language);
        } else if (this.sortCriteria === "license") {
          return a.licenses.localeCompare(b.licenses);
        } else if (this.sortCriteria === "stars") {
          const starsA = a.stars === "No Stars" ? 0 : parseInt(a.stars);
          const starsB = b.stars === "No Stars" ? 0 : parseInt(b.stars);
          return starsB - starsA;
        }
        return 0;
      });
    }
  },
  methods: {
    refreshResults() {
      // Redirect to the Code Input page with the existing code in the query parameter
      this.$router.push({ path: "/", query: { code: this.code } });
    }
  },
  mounted() {
    if (!this.results.length) {
      console.warn("No results received from backend.");
      console.log(this.results); // Check that each result object has a `link` property

    }
  }
  
};
</script>

<style scoped>
.results {
  padding: 20px;
  text-align: center;
  /* background: linear-gradient(135deg, #ffffff, #ffffff);
  min-height: 300vh; */
}
.content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px; /* Add space between left and right sections */
}
.code-display {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 40%;
  position: sticky;
  top: 20px;
}

textarea {
  width: 100%;
  height: 50vh;
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 5px;
  resize: none;
}

button {
  padding: 12px 24px;
  font-size: 16px;
  background-color: #000000;
  color: #fff;
  border: none;
  border-radius: 7px;
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;

}
button:hover {
  background-color: #333;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);

}
.result-list {
  width: 55%;
  text-align: left;
}
ul {
  list-style: none;
  padding: 0;
}

.result-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}
.result-number {
  font-weight: bold;
  font-size: 16px;
  margin-right: 8px;
}
.label {
  font-size: 16px;
  font-weight: bold;
  margin-left: 10px;
  overflow-wrap: break-word; /* Ensure text wraps within the label */
  word-break: break-word;
  white-space: normal;
}
.result-details p {
  margin: 5px 0;
}

/* Highlight border for 100% similarity */
.highlighted-result {
  border-color: red;
}

.star-icon {
  width: 23px; /* Adjust size to be smaller */
  height: 23px;
  vertical-align: middle; /* Align the icon vertically in the middle */
  margin-left: -3px; /* Adjust space between the star icon and star count */
  margin-bottom: 8px; /* Slight adjustment to lower the icon */
}

.result-item {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow-wrap: break-word; /* Ensure text wraps within the frame */
  word-wrap: break-word; /* Break long words */
  white-space: normal; /* Allow text to wrap onto multiple lines */
  box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1); /* Soft shadow */
  transition: transform 0.2s ease;
  background-color: #f8f8f8;
  animation: fadeIn 0.5s ease-in-out;
}

.result-item:hover {
  transform: translateY(-1.5px); /* Slight lift on hover */
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.highlighted-result {
  border-color: #af4c53; /* Green for a positive highlight */
  background-color: #f5e8e8; /* Light green background for 100% similarity */
}

h3 {
  font-size: 1em;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
}

textarea {
  line-height: 1.5;
  padding: 12px;
  font-family: 'Roboto Mono', monospace; /* Add a monospace font for code */

}

.rerank-badge {
  display: inline-block;
  margin-left: 10px;
  padding: 1px 8px;
  border-radius: 5px;
  font-size: 0.8em;
  font-weight: bold;
  background-color: #6366f1;
  color: white;
  white-space: nowrap;
}

.similarity-badge {
  display: inline-block;
  background-color: #e87a7ad2; /* Blue background */
  color: rgb(255, 255, 255);
  padding: 1px 5px;
  border-radius: 5px;
  font-weight: bold;
  font-size: 1.1em;
}

.subtitle {
  font-size: 0.9em;
  color: #555;
  margin-top: -10px;
  margin-bottom: 20px;
}

.code-subtitle {
  font-size: 0.9em;
  color: #555;
  margin-top: -10px;
  margin-bottom: 2px;
}

.small-icon {
  font-size: 0.8rem; /* Adjust the size as needed */
  vertical-align: middle; /* Aligns icon vertically with text */
}

#sortCriteria {
  padding: 8px 12px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
  color: #333;
  cursor: pointer;
  outline: none;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

#sortCriteria:hover {
  background-color: #e6e6e6;
  border-color: #999;
}

#sortCriteria:focus {
  border-color: #007bff;
  background-color: #ffffff;
}

.result-list label {
  font-weight: bold;
  margin-right: 10px;
  color: #555;
  font-size: 14px;
}

.clickable-link {
  color: #327cc6; /* Blue color for links */
  text-decoration: underline; /* Underline for better visibility */
  cursor: pointer; /* Pointer cursor on hover */
}

.clickable-link:hover {
  color: #005bb5; /* Darker blue on hover */
}

</style>
