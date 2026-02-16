import matplotlib.pyplot as plt
import numpy as np
import random
import math
import pandas as pd

class TSP:
    def __init__(self):
        """TSP solver dedicated to the 101-city problem from CSV"""
        filename = '101-City Problem Coordinates.csv'
        
        # ─────────────── CHANGE: Correct CSV loading ───────────────
        df = pd.read_csv(filename, header=None)
        # columns: 0=ID, 1=x, 2=y → we take only 1 and 2
        self.cities = df[[1, 2]].to_numpy().T          # shape (2, 101)
        self.N = self.cities.shape[1]
        
        print(f"Loaded {self.N} cities from {filename}")

        # Random initial tour
        self.tour = list(range(self.N))
        random.shuffle(self.tour)
        
        # Compute initial length
        self.current_length = self.tour_length(self.tour)

        # Keep track of the best solution found
        self.best_tour = self.tour.copy()
        self.best_length = self.current_length

        # Simulated Annealing parameters
        self.T = 300.0           # higher because distances are larger
        self.alpha = 0.999      # slower cooling → better results
        self.max_iter = 20**5   # more moves needed with simple swap

    def tour_length(self, tour):
        """Calculate total Euclidean distance of a tour (including return to start)"""
        total = 0.0
        for i in range(self.N - 1):
            c1 = self.cities[:, tour[i]]
            c2 = self.cities[:, tour[i + 1]]
            total += math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
        
        # Close the loop: last city back to first
        cl = self.cities[:, tour[-1]]
        cf = self.cities[:, tour[0]]
        total += math.sqrt((cl[0] - cf[0])**2 + (cl[1] - cf[1])**2)
        return total

    def solve(self):
        """Run simulated annealing"""
        print("Starting Simulated Annealing...")
                
        for it in range(self.max_iter):
            # 1. Generate neighbor by swapping two random cities
            i = random.randint(0, self.N - 1)
            j = random.randint(0, self.N - 1)
            while i == j:
                j = random.randint(0, self.N - 1)
            
            new_tour = self.tour.copy()
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
            
            # 2. Calculate new length
            new_length = self.tour_length(new_tour)

            # 3. Compute difference
            delta = new_length - self.current_length
            
             # 4. Acceptance decision (this is the core of Simulated Annealing)
            if delta < 0:
                self.tour = new_tour
                self.current_length = new_length
                if new_length < self.best_length:
                    self.best_tour = self.tour.copy()
                    self.best_length = new_length
            else:
                p = math.exp(-delta / self.T)
                if random.random() < p:
                    self.tour = new_tour
                    self.current_length = new_length
            
            # 5. Cool down the temperature
            self.T *= self.alpha

        print(f"\nFinished. Best length: {self.best_length:.2f}")
        return self.best_tour, self.best_length

    def plot(self):
        """Plot the best tour using matplotlib"""
        x = self.cities[0, self.best_tour]
        y = self.cities[1, self.best_tour]

        # Add the closing edge back to start
        x = np.append(x, x[0])
        y = np.append(y, y[0])
        
        plt.figure(figsize=(8, 5))
        plt.scatter(self.cities[0], self.cities[1], c='red', s=35, alpha=0.7, label='Cities')
        
        # ─────────────── CHANGE: 1-based city numbering ───────────────
        for i in range(self.N):
            plt.text(self.cities[0,i] + 0.4, self.cities[1,i] + 0.4, str(i+1), fontsize=7)
        
        plt.plot(x, y, 'b-', linewidth=1.2, alpha=0.9, label='Best Tour')
        plt.title(f"Best TSP Tour (Length = {self.best_length:.2f})")
        plt.xlabel("X coordinate")
        plt.ylabel("Y coordinate")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    solver = TSP()
    best_tour, best_length = solver.solve()
    solver.plot()