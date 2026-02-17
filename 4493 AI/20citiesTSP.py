import matplotlib.pyplot as plt
import numpy as np
import random
import math

class TSP:
    def __init__(self, cities):
        """Initialize the TSP solver with the 20 cities (2 x 20 matrix)"""
        self.cities = np.array(cities)          # shape: (2, 20)
        self.N = 20
        
        # Start with a random tour
        self.tour = list(range(self.N))
        random.shuffle(self.tour)
        
        # Compute initial length
        self.current_length = self.tour_length(self.tour)
        
        # Keep track of the best solution found
        self.best_tour = self.tour.copy()
        self.best_length = self.current_length
        
        # Simulated Annealing parameters
        self.T = 5.0
        self.alpha = 0.995
        self.max_iter = 10**4

    def tour_length(self, tour):
        """Calculate total Euclidean distance of a tour (including return to start)"""
        total = 0.0
        for i in range(self.N - 1):
            c1 = self.cities[:, tour[i]]
            c2 = self.cities[:, tour[i + 1]]
            total += math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
        
        # Close the loop: last city back to first
        c1 = self.cities[:, tour[-1]]
        c2 = self.cities[:, tour[0]]
        total += math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
        return total

    def generate_2opt_neighbor(self, tour):
        """Generate a new tour using a simple 2-opt move (reverses a segment)"""
        new_tour = tour.copy()
        # Choose two distinct positions i < j (at least 2 cities apart)
        i = random.randint(0, self.N - 3)
        j = random.randint(i + 2, self.N - 1)
        
        # Reverse the segment from i+1 to j (inclusive)
        new_tour[i+1:j+1] = new_tour[i+1:j+1][::-1]
        return new_tour

    def solve(self):
        """Run Simulated Annealing with 2-opt neighborhood"""
        print("Starting Simulated Annealing (2-opt)...")
        
        for it in range(self.max_iter):
            # 1. Generate neighbor using 2-opt move
            new_tour = self.generate_2opt_neighbor(self.tour)
            
            # 2. Calculate new length
            new_length = self.tour_length(new_tour)
            
            # 3. Compute difference
            delta = new_length - self.current_length
            
            # 4. Acceptance decision
            if delta < 0:                          # Better solution → always accept
                self.tour = new_tour
                self.current_length = new_length
                
                if self.current_length < self.best_length:
                    self.best_tour = self.tour.copy()
                    self.best_length = self.current_length
                    
            else:                                  # Worse solution → accept with probability
                p = math.exp(-delta / self.T)
                if random.random() < p:
                    self.tour = new_tour
                    self.current_length = new_length
            
            # 5. Cool down the temperature
            self.T *= self.alpha
                    
        print(f"Finished! Best tour length found: {self.best_length:.4f}")
        return self.best_tour, self.best_length

    def plot(self):
        """Plot the best tour using matplotlib"""
        x = self.cities[0, self.best_tour]
        y = self.cities[1, self.best_tour]
        
        # Add the closing edge back to start
        x = np.append(x, x[0])
        y = np.append(y, y[0])
        
        plt.figure(figsize=(8, 8))
        plt.scatter(self.cities[0], self.cities[1], c='red', s=50, label='Cities')
        
        for i, (xi, yi) in enumerate(zip(self.cities[0], self.cities[1])):
            plt.text(xi + 0.01, yi + 0.01, str(i), fontsize=12)
        
        plt.plot(x, y, 'b-', linewidth=2, label='Best Tour')
        plt.title(f"Best TSP Tour (Length = {self.best_length:.4f})")
        plt.xlabel("X coordinate")
        plt.ylabel("Y coordinate")
        plt.legend()
        plt.grid(True)
        plt.show()


# 20 cities here (2 rows × 20 columns)
cities = np.array([
    [0.6606, 0.9695, 0.5906, 0.2124, 0.0398, 0.1367, 0.9536, 0.6091, 0.8767, 0.8148,
     0.9500, 0.6740, 0.5029, 0.8274, 0.9697, 0.5979, 0.2184, 0.7148, 0.2395, 0.2867],
    [0.3876, 0.7041, 0.0213, 0.3429, 0.7471, 0.5449, 0.9464, 0.1247, 0.1636, 0.8668,
     0.8200, 0.3296, 0.1649, 0.3025, 0.8192, 0.9392, 0.8191, 0.4351, 0.8646, 0.6768]
])

if __name__ == "__main__":
    best_length = float('inf')
    best_tour_final = None

    print("Running 20 independent trials with 2-opt neighborhood...\n")

    # Run 20 independent trials and keep track of the best solution found
    for trial in range(20):
        solver = TSP(cities)
        tour, length = solver.solve()
        print(f"Trial {trial+1:2d}: {length:.4f}")
        
        if length < best_length:
            best_length = length
            best_tour_final = tour.copy()

    print(f"\nBest tour length over 20 trials: {best_length:.4f}")

    # Plot the overall best tour
    solver.best_tour = best_tour_final
    solver.best_length = best_length
    solver.plot()