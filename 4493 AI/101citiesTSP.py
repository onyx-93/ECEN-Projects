import matplotlib.pyplot as plt
import numpy as np
import random
import math
import pandas as pd

class TSP:
    def __init__(self):
        """TSP solver for the 101-city problem from CSV with 2-opt neighborhood"""
        filename = '101-City Problem Coordinates.csv'
        
        df = pd.read_csv(filename, header=None)
        self.cities = df[[1, 2]].to_numpy().T          # shape (2, 101)
        self.N = self.cities.shape[1]
        
        print(f"Loaded {self.N} cities from {filename}")

        # Random initial tour
        self.tour = list(range(self.N))
        random.shuffle(self.tour)
        
        self.current_length = self.tour_length(self.tour)
        self.best_tour = self.tour.copy()
        self.best_length = self.current_length

        # Simulated Annealing parameters    
        self.T = 1200.0          # higher starting temp (larger distances)
        self.alpha = 0.9996      # fairly slow cooling – allows good exploration
        self.max_iter = 500000   # 300k is a reasonable compromise for 2-opt

    def tour_length(self, tour):
        """Total Euclidean tour length (closed)"""
        total = 0.0
        for i in range(self.N - 1):
            c1 = self.cities[:, tour[i]]
            c2 = self.cities[:, tour[i + 1]]
            total += math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
        
        cl = self.cities[:, tour[-1]]
        cf = self.cities[:, tour[0]]
        total += math.sqrt((cl[0] - cf[0])**2 + (cl[1] - cf[1])**2)
        return total

    def generate_2opt_neighbor(self, tour):
        """Simple 2-opt move: reverse a random segment"""
        new_tour = tour.copy()
        i = random.randint(0, self.N - 3)
        j = random.randint(i + 2, self.N - 1)
        new_tour[i+1:j+1] = new_tour[i+1:j+1][::-1]
        return new_tour

    def solve(self):
        """Run Simulated Annealing with 2-opt"""
        print("Starting Simulated Annealing (2-opt neighborhood)...")
        
        for it in range(self.max_iter):
            new_tour = self.generate_2opt_neighbor(self.tour)
            new_length = self.tour_length(new_tour)
            delta = new_length - self.current_length
            
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
            
            self.T *= self.alpha

        print(f"\nFinished. Best length: {self.best_length:.2f}")
        return self.best_tour, self.best_length

    def plot(self):
        """Plot the best tour"""
        x = self.cities[0, self.best_tour]
        y = self.cities[1, self.best_tour]
        x = np.append(x, x[0])
        y = np.append(y, y[0])
        
        plt.figure(figsize=(10, 10))
        plt.scatter(self.cities[0], self.cities[1], c='red', s=35, alpha=0.7, label='Cities')
        
        for i in range(self.N):
            plt.text(self.cities[0,i] + 0.4, self.cities[1,i] + 0.4, str(i+1), fontsize=7)
        
        plt.plot(x, y, 'b-', linewidth=1.2, alpha=0.9, label='Best Tour')
        plt.title(f"Best TSP Tour (Length = {self.best_length:.4f})")
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