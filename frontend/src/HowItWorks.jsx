import hackuuuImage from "/image1.jpeg";
import hackuuuImage2 from "/image2.jpeg";
import hackuuuImage3 from "/image3.jpeg";

export default function HowItWorks() {
  return (
    <section
      id="how-it-works"
      className="py-24 px-6 bg-white border-t border-gray-200"
    >

      <div className="max-w-5xl mx-auto text-center">

        {/* Title */}
        <h2 className="text-5xl font-bold text-blue-600 tracking-tight">
          How Smurf-Proof Works
        </h2>

        <p className="text-gray-500 mt-4 text-lg max-w-xl mx-auto">
          From raw transactions to intelligent graph-based AML insights.
        </p>

        {/* Divider */}
        <div className="w-16 h-1 bg-blue-500 rounded-full mx-auto mt-6 mb-14"></div>

        {/* USER FLOW */}

        <div className="text-left">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">
            User Flow
          </h2>
        </div>

        <div className="grid md:grid-cols-3 gap-8 text-left">

          {/* Card 1 */}
          <div className="bg-blue-50 border border-blue-100 rounded-2xl p-7 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">

            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              1. Upload Transactions
            </h3>

            <p className="text-sm text-gray-600">
              Upload a CSV containing transaction relationships. The system
              validates structure and prepares graph nodes & edges.
            </p>

          </div>

          {/* Card 2 */}
          <div className="bg-blue-50 border border-blue-100 rounded-2xl p-7 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">

            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              2. Analyze Graph
            </h3>

            <p className="text-sm text-gray-600">
              Transactions are converted into a graph and analyzed using AML
              heuristics to detect suspicious patterns and clusters.
            </p>

          </div>

          {/* Card 3 */}
          <div className="bg-blue-50 border border-blue-100 rounded-2xl p-7 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">

            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              3. Investigate Visually
            </h3>

            <p className="text-sm text-gray-600">
              Explore an interactive live graph to identify risky wallets,
              abnormal flows, and hidden connections instantly.
            </p>

          </div>

        </div>

        {/* HOW IT WORKS SECTION */}

        <div className="text-left mt-20">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">
            How it works behind the scene
          </h2>
        </div>

        <div className="flex flex-row gap-6 text-left">

          {/* Diagram */}
          <div className="w-140 h-66 border border-gray-200 overflow-hidden rounded-xl shadow-md bg-white">

            <img
              src={hackuuuImage}
              alt="diagram"
              className="w-full h-full object-contain"
            />

          </div>

          {/* Core Ideas */}
          <div className="bg-blue-50 border border-blue-100 rounded-2xl p-6 shadow-sm hover:shadow-lg transition w-90 h-66">

            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Core Ideas
            </h3>

            <p className="text-sm text-gray-600">
              The fundamental idea of the system is to represent blockchain transactions as a directed weighted graph
              We model blockchain transactions as a temporal directed graph and apply hybrid intelligence:<br />
              1. Graph Construction<br />
              Wallets → nodes<br />
              Transactions → directed edges (amount + time)<br />
              2. Rule-Based Graph Pattern Detection</p>

          </div>

        </div>

        {/* Explanation */}

        <div className="bg-blue-50 border border-blue-100 rounded-2xl p-8 mt-10 shadow-sm hover:shadow-lg transition text-left">

          <p className="text-sm text-gray-600">
          We combine rule-based AML signals with a graph neural network–based propagation approach to compute a final risk score for each wallet. The rule engine captures explicit laundering behaviors such as fan-in, fan-out, pass-through flow, and suspicious timing, ensuring interpretability and regulatory alignment. The CPU-based GNN then propagates this risk through the transaction graph, allowing indirect and hidden relationships to influence wallet suspicion. By fusing both perspectives, the final risk score balances explainable rule violations with relational intelligence from the network structure, resulting in a more robust, scalable, and realistic money-laundering detection system.
          
          </p>

        </div>

        {/* FORMULA SECTION */}

        <div className="flex flex-row gap-6 mt-12 text-left">

          <div className="w-140 border border-gray-200 overflow-hidden rounded-xl shadow-md bg-white">

            <img
              src={hackuuuImage2}
              alt="formula"
              className="w-full h-full object-contain"
            />

          </div>

          <div className="pt-4">

            <div className="bg-blue-50 border border-blue-100 rounded-2xl p-6 shadow-sm hover:shadow-md transition w-90 mt-3">

              <p className="text-sm text-gray-600">
               R(w)=αS(w)+βF(w)+γT(w)+δP(w)
                where:<br />
                S(w)= Structural Risk<br />
                F(w)= Flow Risk<br />
                T(w)= Temporal Risk<br />
                P(w)= Proximity Risk<br />
                α,β,γ,δare weighting coefficients such that
                α+β+γ+δ=1
              </p>

            </div>

            <div className="bg-blue-50 border border-blue-100 rounded-2xl p-6 shadow-sm hover:shadow-md transition w-90 mt-3">

              <p className="text-sm text-gray-600">
               In structural Risk<br />
                "fan_in"(w)= normalized in-degree of wallet w<br />
                "fan_out"(w)= normalized out-degree of wallet w
              </p>

            </div>

            <div className="bg-blue-50 border border-blue-100 rounded-2xl p-6 shadow-sm hover:shadow-md transition w-90 mt-3">

              <p className="text-sm text-gray-600">
               In Flow Risk<br />
                ε is a small threshold<br />
                "inflow"(w)and "outflow"(w)represent total transaction value
              </p>

            </div>

            <div className="bg-blue-50 border border-blue-100 rounded-2xl p-6 shadow-sm hover:shadow-md transition w-90 mt-3">

              <p className="text-sm text-gray-600">
                In Temproal Risk<br />
                Δt=t_2-t_1is a short time window<br />
                High temporal risk indicates rapid fund movement
              </p>

            </div>

            <div className="bg-blue-50 border border-blue-100 rounded-2xl p-6 shadow-sm hover:shadow-md transition w-90 mt-3">

              <p className="text-sm text-gray-600">
In Proximity Risk<br />
                Proximity risk captures the influence of nearby suspicious wallets in the transaction graph.
                P(w)=1/(d(w)+1)
              </p>

            </div>

          </div>

        </div>

        {/* GNN SECTION */}

        <div className="flex flex-row gap-6 mt-14 text-left">

          <div>

            <h3 className="text-xl font-bold text-gray-900">
              Risk Computation by CPU-based GNN
            </h3>

            <div className="w-140 h-94 border border-gray-200 overflow-hidden mt-6 rounded-xl shadow-md bg-white">

              <img
                src={hackuuuImage3}
                alt="gnn"
                className="w-full h-full object-contain"
              />

            </div>

          </div>

          <div className="bg-blue-50 border border-blue-100 rounded-2xl p-6 shadow-sm hover:shadow-lg transition w-90 mt-12">

            <p className="text-sm text-gray-600">
              v = wallet being updated  
              <br /><br />
              N(v) = neighboring wallets  
              <br /><br />
              hᵤ(l) = feature representation  
              <br /><br />
              W = learnable weight  
              <br /><br />
              σ = non-linear activation
            </p>

          </div>

        </div>

        {/* CONCLUSION */}

        <div className="bg-blue-50 border border-blue-100 rounded-2xl p-8 mt-16 shadow-sm hover:shadow-lg transition text-left">

          <h3 className="text-gray-900 font-semibold mb-3">
            Conclusion
          </h3>

          <p className="text-sm text-gray-600">
            By combining rule-based AML signals with graph neural propagation,
            the system detects hidden laundering structures across blockchain
            transaction networks while maintaining interpretability and
            scalability.
          </p>

        </div>

      </div>
    </section>
  );
}