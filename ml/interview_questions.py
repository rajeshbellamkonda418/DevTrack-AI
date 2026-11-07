INTERVIEW_QUESTIONS = {
    "genai": {
        "name": "Generative AI & LLMs",
        "questions": {
            "basic": [
                ("What is a large language model (LLM)?", "An LLM is a neural network trained on large text datasets to predict and generate sequences of tokens. Its responses are generated from learned patterns, not a live database of facts."),
                ("What is the difference between a prompt and a completion?", "A prompt is the input and instructions supplied to a model. A completion is the model-generated output that follows that input."),
            ],
            "intermediate": [
                ("How does retrieval-augmented generation (RAG) reduce unsupported answers?", "RAG retrieves relevant passages from an external knowledge source and includes them in the model's context. The model can then ground its response in those passages, though retrieval quality and prompt design still matter."),
                ("What are embeddings, and how are they used in semantic search?", "Embeddings map text into numeric vectors whose distances represent aspects of semantic similarity. A search system embeds a query and compares it with stored document vectors to retrieve relevant content."),
            ],
            "advanced": [
                ("How would you evaluate a RAG system beyond checking answer fluency?", "Evaluate retrieval separately (such as recall@k and ranking quality) and generation for groundedness, relevance, completeness, and citation correctness. Use representative test sets and human review, and track latency and cost."),
                ("When would you choose fine-tuning over RAG?", "Use fine-tuning when you need the model to consistently learn a task format, style, or behavior from examples. Use RAG when the model needs access to changing or private factual content; the approaches can also be combined."),
            ],
        },
    },
    "machine-learning": {
        "name": "Machine Learning",
        "questions": {
            "basic": [
                ("What is the difference between supervised and unsupervised learning?", "Supervised learning learns from labeled input-output examples. Unsupervised learning looks for structure in data without target labels, for example clusters or lower-dimensional representations."),
                ("What is overfitting?", "Overfitting occurs when a model fits training-specific patterns, including noise, and performs poorly on unseen data. More representative data, regularization, and appropriate validation can help."),
            ],
            "intermediate": [
                ("Why do we split data into training, validation, and test sets?", "Training data fits model parameters, validation data guides model and hyperparameter choices, and the test set estimates final generalization. Reusing the test set during tuning leaks information and biases the estimate."),
                ("How do precision and recall differ, and when might each matter more?", "Precision is the fraction of predicted positives that are correct; recall is the fraction of actual positives found. Precision matters when false alarms are costly, while recall matters when missing a positive case is costly."),
            ],
            "advanced": [
                ("How would you detect and prevent target leakage in a time-dependent prediction task?", "Audit every feature's availability timestamp and ensure it would exist at prediction time. Use chronological splits, fit preprocessing only on training data, and remove features or transformations derived from future outcomes."),
                ("A model's offline score is strong but production performance drops. How would you investigate?", "Check for data and concept drift, training-serving skew, label delays, and differences in sampling or preprocessing. Compare production feature distributions and segment-level metrics, then validate fixes with a representative time-based evaluation."),
            ],
        },
    },
    "python": {
        "name": "Python",
        "questions": {
            "basic": [
                ("What is the difference between a list and a tuple in Python?", "Both are ordered sequences, but lists are mutable and tuples are immutable. Tuples can represent fixed records and may be hashable when all their elements are hashable."),
                ("What is a dictionary, and what are its typical lookup characteristics?", "A dictionary maps hashable keys to values. Key lookup is typically O(1) on average, though collisions and resizing affect implementation details."),
            ],
            "intermediate": [
                ("What is a generator, and when is it useful?", "A generator yields values lazily, commonly using yield, rather than building the entire result in memory. It is useful for large inputs, streaming, or pipelines where values are consumed incrementally."),
                ("What is a context manager?", "A context manager defines setup and cleanup around a with block, usually through __enter__ and __exit__ or a contextlib helper. It helps reliably release resources such as files and locks, including when exceptions occur."),
            ],
            "advanced": [
                ("What is the Global Interpreter Lock (GIL), and how does it affect concurrency?", "In CPython, the GIL ensures only one thread executes Python bytecode at a time in a process. Threads can still help with I/O-bound work; multiprocessing or native code that releases the GIL can help with CPU-bound parallelism."),
                ("How do mutable default arguments cause bugs, and what is the idiomatic fix?", "Default argument expressions are evaluated once when the function is defined, so a mutable default is shared between calls. Use None as the default and create a fresh list or dictionary inside the function."),
            ],
        },
    },
    "sql": {
        "name": "SQL & Databases",
        "questions": {
            "basic": [
                ("What is the difference between WHERE and HAVING?", "WHERE filters rows before grouping and aggregation. HAVING filters groups after GROUP BY and can use aggregate results."),
                ("What does a primary key guarantee?", "A primary key uniquely identifies each row and cannot contain NULL values. A table has one primary-key constraint, which may consist of multiple columns."),
            ],
            "intermediate": [
                ("How does a LEFT JOIN differ from an INNER JOIN?", "An INNER JOIN returns rows with matches on both sides. A LEFT JOIN preserves every row from the left side and fills right-side columns with NULL when there is no match."),
                ("What is an index, and what trade-offs does it introduce?", "An index is an auxiliary structure that can speed up filtering, joining, or ordering. It consumes storage and adds work to writes and maintenance, so indexes should match real query patterns."),
            ],
            "advanced": [
                ("How would you find each customer's most recent order in SQL?", "A common approach is ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, id DESC) in a subquery or CTE, then filter to row number 1. The extra tie-breaker makes selection deterministic."),
                ("What does transaction isolation protect against, and what is a trade-off of stronger isolation?", "Isolation controls how concurrent transactions observe one another and helps prevent anomalies such as dirty reads or inconsistent updates. Stronger isolation can reduce anomalies but may increase locking, retries, or contention."),
            ],
        },
    },
    "data-structures": {
        "name": "Data Structures & Algorithms",
        "questions": {
            "basic": [
                ("When would you use a queue instead of a stack?", "A queue processes items in first-in, first-out order, which suits scheduling and breadth-first search. A stack is last-in, first-out and suits call stacks, undo operations, and depth-first traversal."),
                ("What does Big O notation describe?", "Big O describes how an algorithm's resource use grows asymptotically with input size, commonly time or space. It abstracts away constant factors and lower-order terms."),
            ],
            "intermediate": [
                ("How would you detect a cycle in a linked list with O(1) extra space?", "Use Floyd's tortoise-and-hare algorithm: advance one pointer by one node and another by two. If they meet, there is a cycle; if the fast pointer reaches the end, there is not."),
                ("When can binary search be used, and what is its time complexity?", "Binary search needs a search space with an ordering or monotonic predicate that lets each comparison discard half the remaining candidates. Its time complexity is O(log n) for a random-access sorted array."),
            ],
            "advanced": [
                ("How can you find the top k elements in a very large stream?", "Maintain a size-k min-heap, adding each item and removing the smallest when the heap exceeds k. This uses O(k) space and O(n log k) time; approximate sketches are an option when even that memory is too costly."),
                ("What is the difference between amortized and average-case complexity?", "Average-case complexity depends on a probability distribution over inputs or operations. Amortized complexity bounds the total cost of a sequence of operations, even when individual operations can be expensive."),
            ],
        },
    },
    "web-backend": {
        "name": "Web & Backend Engineering",
        "questions": {
            "basic": [
                ("What is the difference between an HTTP GET and POST request?", "GET requests retrieve a representation and should not change server state; POST submits data for processing and may change state. GET parameters are commonly placed in the URL, while POST data is typically in the request body."),
                ("What does a 404 HTTP status code mean?", "404 means the server could not find a representation for the requested resource. It does not necessarily mean the server itself is unavailable."),
            ],
            "intermediate": [
                ("Why should a create-payment endpoint consider idempotency?", "Clients may retry requests after timeouts even if the first request succeeded. An idempotency key lets the server recognize retries and avoid creating duplicate charges or operations."),
                ("What is the role of a database connection pool?", "A pool reuses a bounded set of database connections rather than opening one for every request. It reduces connection setup cost and helps control database concurrency, but its size and timeout behavior need tuning."),
            ],
            "advanced": [
                ("How would you design a rate limiter for a distributed API?", "Choose a policy such as token bucket or sliding window, key it by an authenticated client or other trusted identity, and store coordinated state in a shared low-latency service. Define behavior under store failure and consider atomic updates, burst limits, and observability."),
                ("How do you make a background job safe to retry?", "Make processing idempotent where possible, use a stable job identifier or deduplication key, and commit side effects transactionally or through an outbox pattern. Bound retries and route persistent failures to a dead-letter or review path."),
            ],
        },
    },
    "data-engineering": {
        "name": "Data Engineering",
        "questions": {
            "basic": [
                ("What is the difference between ETL and ELT?", "ETL transforms data before loading it into the target. ELT loads raw data first and performs transformations in the target system, often taking advantage of its compute and storage."),
                ("What is a data pipeline?", "A data pipeline is a sequence of steps that moves and transforms data between systems, with scheduling or triggering, validation, error handling, and monitoring."),
            ],
            "intermediate": [
                ("What is the difference between batch and stream processing?", "Batch processing operates on bounded collections at intervals, while stream processing handles events continuously or in small windows. The choice depends on latency, ordering, and operational requirements."),
                ("Why are data quality checks important in a pipeline?", "They detect issues such as missing values, schema changes, duplicates, or invalid ranges before bad data propagates. Checks should have clear failure or quarantine behavior and visible alerts."),
            ],
            "advanced": [
                ("How would you handle duplicate events in an at-least-once delivery system?", "Assume duplicates are possible and make consumers idempotent using an event identifier or a natural deduplication key. Persist processed identifiers or use transactional writes, with retention aligned to replay requirements."),
                ("How would you evolve a production data schema without breaking consumers?", "Use backward-compatible changes first, such as adding nullable fields with defaults, and version or coordinate breaking changes. Validate consumers, publish schema contracts, and provide a migration and rollback window."),
            ],
        },
    },
    "cloud-devops": {
        "name": "Cloud & DevOps",
        "questions": {
            "basic": [
                ("What is the difference between a container and a virtual machine?", "A virtual machine runs a guest operating system on virtualized hardware. A container isolates processes while sharing the host kernel, so it is generally lighter and starts faster."),
                ("What is CI/CD?", "Continuous integration frequently validates changes through automated builds and tests. Continuous delivery or deployment automates releasing validated changes, with deployment distinguishing automatic production rollout."),
            ],
            "intermediate": [
                ("Why should application secrets not be stored in a container image?", "Images can be copied, cached, and retained, making embedded credentials difficult to revoke and easy to expose. Inject secrets at runtime from a managed secret store and restrict access by identity."),
                ("What is the difference between liveness and readiness probes?", "A liveness probe indicates whether a process should be restarted. A readiness probe indicates whether it can receive traffic; a failing readiness check should remove it from service without necessarily restarting it."),
            ],
            "advanced": [
                ("How would you investigate rising latency in a microservice system?", "Use traces to find the slow span, then correlate latency percentiles with dependency timings, saturation, errors, and recent changes. Check queueing, connection pools, and resource limits; mitigate safely while preserving diagnostic data."),
                ("How do you design a deployment to reduce risk and enable rollback?", "Use staged or canary rollout with health and business-metric checks, keep the previous version deployable, and define automatic pause or rollback thresholds. Make database changes backward compatible across the rollout window."),
            ],
        },
    },
    "java": {
        "name": "Java",
        "questions": {
            "basic": [
                ("What is the difference between JDK, JRE, and JVM?", "The JVM runs Java bytecode. The JRE provides the JVM and runtime libraries. The JDK includes development tools such as the compiler in addition to the runtime."),
                ("What is the difference between == and equals() in Java?", "For object references, == checks whether both references point to the same object. equals() checks logical equality when a class implements it appropriately; primitive == compares values."),
            ],
            "intermediate": [
                ("When would you use an interface instead of an abstract class?", "Use an interface to define a capability or contract that unrelated classes can implement. Use an abstract class when closely related classes should share state or implementation; Java classes can implement multiple interfaces but extend only one class."),
                ("How do HashMap and ConcurrentHashMap differ?", "HashMap is not safe for unsynchronized concurrent mutation. ConcurrentHashMap supports concurrent access with thread-safe operations, but compound operations still need atomic methods such as computeIfAbsent."),
            ],
            "advanced": [
                ("Why should equals() and hashCode() be overridden consistently?", "Objects that are equal according to equals() must have the same hashCode(). Hash-based collections use the hash to locate entries, so violating the contract can make logically equal keys fail lookups."),
                ("How would you diagnose excessive garbage collection pauses in a Java service?", "Inspect GC logs and pause distributions, heap occupancy, allocation rate, and object-retention paths. Use profiling or heap dumps to identify allocation hot spots or leaks, then validate collector and heap changes against workload metrics."),
            ],
        },
    },
    "cybersecurity": {
        "name": "Cybersecurity",
        "questions": {
            "basic": [
                ("What is the principle of least privilege?", "Give each user, service, and process only the permissions needed for its task, for only as long as needed. This limits the damage if an account or component is compromised."),
                ("How do authentication and authorization differ?", "Authentication establishes who or what is making a request. Authorization decides which actions that identity is permitted to perform."),
            ],
            "intermediate": [
                ("Why should passwords be hashed with a unique salt?", "A salt makes identical passwords produce different stored hashes and defeats precomputed rainbow tables. Passwords should use a deliberately slow, password-specific hash such as Argon2id, bcrypt, or scrypt."),
                ("How does parameterized SQL help protect an application?", "Parameterized queries keep user-provided values separate from SQL syntax, preventing those values from being interpreted as executable query fragments. Input validation and least-privilege database access provide additional defenses."),
            ],
            "advanced": [
                ("How would you respond to a suspected leaked production credential?", "Revoke or rotate it immediately, identify affected systems and access logs, and contain suspicious sessions. Preserve evidence, assess exposure, restore services safely, and investigate how the credential was stored or disclosed to prevent recurrence."),
                ("What security properties should a robust session design include?", "Use unpredictable session identifiers, secure and HttpOnly cookies, appropriate SameSite settings, TLS, expiration and rotation, and server-side invalidation. Rotate identifiers after authentication or privilege changes and protect against CSRF where relevant."),
            ],
        },
    },
    "frontend": {
        "name": "Frontend Engineering",
        "questions": {
            "basic": [
                ("What is semantic HTML, and why does it matter?", "Semantic elements describe the purpose of their content, such as nav, main, and button. They improve accessibility, browser behavior, and document structure for assistive technology and search tools."),
                ("What is the difference between let, const, and var in JavaScript?", "let and const are block-scoped; const prevents reassignment of the binding, not mutation of an object it references. var is function-scoped and has older hoisting behavior, so modern code generally favors let and const."),
            ],
            "intermediate": [
                ("What causes a stale closure in a UI event handler?", "A closure captures values from the render or scope where it was created. If a long-lived callback uses an outdated captured value, use an updated dependency, functional state update, or another design that reads current state."),
                ("How would you improve a page that renders thousands of rows?", "Virtualize the list so only visible rows are rendered, paginate or filter data where appropriate, and avoid unnecessary re-renders. Measure actual rendering and interaction performance before optimizing."),
            ],
            "advanced": [
                ("How do you prevent cross-site scripting when displaying user-generated text?", "Prefer DOM text APIs or framework-escaped text interpolation instead of building HTML strings. If rich HTML is required, sanitize it with a well-maintained allowlist sanitizer and apply a defense-in-depth Content Security Policy."),
                ("How would you investigate and reduce layout shift on a page?", "Use performance tooling to identify layout-shift sources, then reserve space for images and embeds, avoid inserting content above existing content, and use stable font loading and layout dimensions. Check the user-visible CLS metric."),
            ],
        },
    },
    "system-design": {
        "name": "System Design",
        "questions": {
            "basic": [
                ("What is the difference between horizontal and vertical scaling?", "Vertical scaling adds resources to one machine; horizontal scaling adds more machines or instances. Horizontal scaling can improve capacity and resilience but often requires handling distributed state and coordination."),
                ("What is a cache, and what is one common risk when using it?", "A cache stores reusable results to reduce latency or load on a source system. Stale data is a common risk, so a design needs an invalidation, expiration, or refresh strategy that suits the data."),
            ],
            "intermediate": [
                ("How would you design a URL shortener at a high level?", "Define APIs and redirect behavior, generate collision-safe short identifiers, store identifier-to-URL mappings, and cache hot redirects. Address expiration, abuse controls, analytics, availability, and read/write scaling."),
                ("What is the difference between a load balancer and a reverse proxy?", "A reverse proxy accepts requests on behalf of backend servers and can handle routing, TLS, and policy. A load balancer distributes requests across healthy targets; many modern reverse proxies also perform load balancing."),
            ],
            "advanced": [
                ("How would you preserve event ordering for updates to the same account?", "Partition events by account key and process each partition sequentially, while allowing different partitions to run concurrently. Define retry, deduplication, and rebalancing behavior so ordering is not silently broken."),
                ("How would you design a highly available service that depends on a slower downstream API?", "Set bounded timeouts, concurrency limits, and backpressure; isolate calls with bulkheads and use retries only when safe with jitter and budgets. Consider caching or graceful degradation, and monitor dependency health and user-facing outcomes."),
            ],
        },
    },
}

ADDITIONAL_QUESTIONS = {
    "genai": {
        "basic": [
            ("What is a token in a language model?", "A token is a unit of text, such as a word, part of a word, or punctuation, that the model processes. Tokenization affects how much context fits in a model's context window."),
        ],
        "intermediate": [
            ("Why can a larger context window still fail to improve an LLM answer?", "A larger window allows more input, but irrelevant or poorly ordered context can distract the model. Retrieval quality, clear instructions, and testing for context position effects remain important."),
        ],
        "advanced": [
            ("How would you reduce prompt-injection risk in a RAG application?", "Treat retrieved content as untrusted data, separate it from instructions, and limit tools and permissions available to the model. Validate outputs and tool arguments outside the model, and test with adversarial documents."),
        ],
    },
    "machine-learning": {
        "basic": [
            ("What is a feature in a machine-learning dataset?", "A feature is an input variable used by a model to make a prediction, such as a transaction amount or product category. Features should be available at prediction time and prepared consistently."),
        ],
        "intermediate": [
            ("Why can accuracy be misleading on an imbalanced dataset?", "A model can predict the majority class every time and still achieve high accuracy while missing the rare class. Examine precision, recall, F1, PR-AUC, and the costs of different errors."),
        ],
        "advanced": [
            ("How would you calibrate probabilities from a classifier?", "Evaluate calibration on held-out data with reliability curves or scores such as Brier score. Apply methods such as Platt scaling or isotonic regression using validation data, then recheck calibration across relevant segments."),
        ],
    },
    "python": {
        "basic": [
            ("What is the difference between == and is in Python?", "== checks whether two values are equal, while is checks whether two references point to the same object. Use is None for the None singleton, not for general value comparison."),
        ],
        "intermediate": [
            ("What do *args and **kwargs collect in a Python function?", "*args collects extra positional arguments into a tuple, while **kwargs collects extra keyword arguments into a dictionary. They are useful for deliberate flexible APIs and argument forwarding."),
        ],
        "advanced": [
            ("When would asyncio be preferable to threads in Python?", "Asyncio is useful for handling many concurrent I/O operations when the libraries support non-blocking awaits. It uses cooperative scheduling in an event loop; CPU-bound work still needs a process, thread, or native implementation."),
        ],
    },
    "sql": {
        "basic": [
            ("How do COUNT(*) and COUNT(column_name) differ?", "COUNT(*) counts rows, including rows with NULL values in individual columns. COUNT(column_name) counts only rows where that column is not NULL."),
        ],
        "intermediate": [
            ("What is a window function, and how is it different from GROUP BY?", "A window function calculates over related rows while retaining each input row, using an OVER clause. GROUP BY collapses rows into one row per group."),
        ],
        "advanced": [
            ("How would you safely paginate a large, frequently changing table?", "Use keyset pagination with a stable, indexed ordering key and a cursor containing the last-seen key values. It avoids many costs and inconsistencies of large OFFSET values, provided the ordering is deterministic."),
        ],
    },
    "data-structures": {
        "basic": [
            ("What is the difference between an array and a linked list?", "Arrays provide constant-time indexed access but may require shifting elements for insertion. Linked lists support local insertions when a node is known, but accessing an arbitrary position requires traversal."),
        ],
        "intermediate": [
            ("How can a queue be implemented efficiently using a fixed-size array?", "Use a circular buffer with head, tail, and size indices. Wrap indices modulo capacity so dequeue does not shift every remaining element."),
        ],
        "advanced": [
            ("How would you find the lowest common ancestor of two nodes in a binary search tree?", "Starting at the root, move left if both target values are smaller and right if both are larger. The first node where the targets split, or one equals the current node, is their lowest common ancestor."),
        ],
    },
    "web-backend": {
        "basic": [
            ("What does a 401 HTTP response mean, and how does it differ from 403?", "401 indicates the request lacks valid authentication credentials. 403 indicates the server understood the request but refuses access, commonly because the authenticated identity lacks permission."),
        ],
        "intermediate": [
            ("Why should an API validate input on the server even when the browser validates forms?", "Client-side checks improve usability but can be bypassed by direct requests or modified clients. Server-side validation enforces the application's trust boundary and protects data and downstream systems."),
        ],
        "advanced": [
            ("How can an application keep a database update and a published event consistent?", "A transactional outbox writes the business change and an event record in the same database transaction. A separate publisher delivers outbox records and marks them sent, with consumers designed to handle retries and duplicates."),
        ],
    },
    "data-engineering": {
        "basic": [
            ("What is a data warehouse used for?", "A data warehouse stores integrated, structured data optimized for analytical queries and reporting. It is generally designed for analysis rather than the short transactional operations of an application database."),
        ],
        "intermediate": [
            ("What does idempotency mean in a data pipeline?", "An idempotent pipeline can process the same input again without creating additional incorrect effects. This supports retries and reprocessing, often through stable keys, deterministic transformations, and safe upserts."),
        ],
        "advanced": [
            ("How would you handle late-arriving events in a windowed stream?", "Define an allowed lateness period and watermark based on event time, then update or emit revised window results while that period remains open. Specify what happens to events arriving after the watermark and monitor their volume."),
        ],
    },
    "cloud-devops": {
        "basic": [
            ("What is infrastructure as code?", "Infrastructure as code describes infrastructure in version-controlled, repeatable configuration that tools can validate and apply. It helps review changes and reduce manual configuration drift."),
        ],
        "intermediate": [
            ("What is the purpose of a health check in a load-balanced service?", "Health checks help a platform decide whether an instance can receive traffic or should be restarted. Checks should reflect meaningful readiness and avoid making transient dependency issues cause widespread restart loops."),
        ],
        "advanced": [
            ("How would you recover a service after an availability-zone failure?", "Distribute capacity across independent zones, detect the failure, and route traffic only to healthy capacity. Validate that surviving capacity, data replication, and automated recovery meet the service's RTO and RPO targets."),
        ],
    },
    "java": {
        "basic": [
            ("What is method overloading in Java?", "Overloading defines multiple methods with the same name but different parameter lists. The compiler selects an overload based on the method call's argument types and arity."),
        ],
        "intermediate": [
            ("Why are String objects immutable in Java?", "Immutability makes strings safe to share, supports string pooling, and ensures their hash value remains stable. Operations that appear to modify a string create a new string instead."),
        ],
        "advanced": [
            ("What is the difference between a synchronized block and a ReentrantLock?", "Both can provide mutual exclusion, but ReentrantLock offers explicit lock management, interruptible and timed acquisition, and optional fairness. Locks must be released in a finally block; synchronized releases automatically."),
        ],
    },
    "cybersecurity": {
        "basic": [
            ("Why should a website use HTTPS?", "HTTPS protects the confidentiality and integrity of traffic between the browser and server and helps authenticate the server. It does not by itself make an application or endpoint trustworthy."),
        ],
        "intermediate": [
            ("What is multi-factor authentication?", "MFA requires evidence from more than one factor category, typically something known, possessed, or inherent. It reduces reliance on a password alone, especially when stronger phishing-resistant factors are used."),
        ],
        "advanced": [
            ("How would you prioritize vulnerabilities found in a software dependency scan?", "Consider exploitability and known exploitation, exposure, affected versions, reachable code paths, and impact to the specific service. Verify findings, prioritize mitigations or upgrades, and track residual risk rather than sorting only by a generic severity score."),
        ],
    },
    "frontend": {
        "basic": [
            ("What is the purpose of the alt attribute on an image?", "Alt text provides a textual equivalent for meaningful images to users of assistive technology and when images cannot load. Decorative images should generally have empty alt text so they are skipped."),
        ],
        "intermediate": [
            ("What is event delegation in JavaScript?", "Event delegation attaches a handler to a common ancestor and uses event bubbling to handle events from its descendants. It can reduce listeners for dynamic lists, but the handler should check the event target carefully."),
        ],
        "advanced": [
            ("How would you diagnose a hydration mismatch in a server-rendered app?", "Compare the server-rendered markup with the first client render and look for nondeterministic values, environment-specific branches, or data differences. Make the initial render deterministic and defer browser-only state until after hydration."),
        ],
    },
    "system-design": {
        "basic": [
            ("What is the role of a database in a typical web application?", "A database persists application data and supports retrieval and updates through defined queries and consistency guarantees. Its schema and access patterns should fit the application's operational and analytical needs."),
        ],
        "intermediate": [
            ("When might you choose eventual consistency over strong consistency?", "Eventual consistency can improve availability, latency, or independent scaling when temporary replica disagreement is acceptable. Choose it only when the user experience and business rules tolerate stale reads and reconciliation."),
        ],
        "advanced": [
            ("How would you design a rate limiter for an API with multiple server instances?", "Use shared or partitioned coordination so instances enforce a consistent policy, such as token bucket or sliding window. Define atomic updates, key identity, burst behavior, failure mode, and what happens when the limiter store is unavailable."),
        ],
    },
}

for topic_id, levels in ADDITIONAL_QUESTIONS.items():
    for level, questions in levels.items():
        INTERVIEW_QUESTIONS[topic_id]["questions"][level].extend(questions)

PYTHON_SQL_QUESTIONS = {
    "python": {
        "basic": [
            ("How do sets differ from lists in Python?", "A list is ordered and allows duplicate values, while a set stores unique hashable values and does not provide positional indexing. Sets are useful for membership checks and set operations."),
            ("What does enumerate() do?", "enumerate() returns an iterator of index-value pairs for an iterable. It is often clearer and safer than maintaining a separate counter in a loop."),
            ("How does slicing work in Python?", "A slice selects items using start:stop:step, where the stop index is excluded. Negative indices count from the end, and a negative step can traverse a sequence in reverse."),
            ("What is the difference between a module and a package?", "A module is a Python file that can define code and names. A package organizes modules under a directory and can expose subpackages and shared interfaces."),
            ("How do you check whether a key exists in a dictionary?", "Use `key in mapping` to test for a key. This checks key membership directly and is preferable to retrieving a value when the value itself could be None."),
            ("What is a list comprehension?", "A list comprehension constructs a list from an iterable with an optional filter, such as `[x * 2 for x in values if x > 0]`. For very large or lazy sequences, a generator expression may use less memory."),
            ("What does the `pass` statement do?", "`pass` is a no-op statement used where Python syntax requires a statement but no action is needed yet, such as an intentionally empty function or class body."),
            ("How does `range()` behave in a for loop?", "`range(stop)` produces integers from zero up to but not including stop. It can also take a start and step, and it represents a range lazily rather than building a list of all values."),
        ],
        "intermediate": [
            ("What is the difference between a shallow copy and a deep copy?", "A shallow copy creates a new outer object but keeps references to nested objects. A deep copy recursively copies nested contents, though custom objects may require special handling."),
            ("What is a decorator in Python?", "A decorator is a callable that takes a function or class and returns a replacement, often to add behavior such as logging or access checks. The `@decorator` syntax applies it when the definition is created."),
            ("How does Python's iterator protocol work?", "An iterable provides `__iter__()` to return an iterator. An iterator provides `__next__()` to return each item and raises StopIteration when exhausted; a for loop uses this protocol."),
            ("When would you use a dataclass?", "A dataclass can generate common methods such as initialization and representation from annotated fields. It is useful for data-oriented classes, while validation or complex invariants may call for explicit methods or another model."),
            ("What is the purpose of `__slots__`?", "`__slots__` declares a fixed set of instance attributes and can reduce per-instance memory by avoiding a normal instance dictionary. It changes dynamic attribute behavior and should be used only when its trade-offs are appropriate."),
            ("How should a Python program manage resources such as files?", "Use a context manager, commonly with a `with` statement, so cleanup runs reliably even if an exception occurs. Custom resource types can implement the context manager protocol or use contextlib helpers."),
            ("What is the difference between `@classmethod` and `@staticmethod`?", "A class method receives the class as its first argument and can provide alternate constructors or class-level behavior. A static method receives no implicit instance or class and is a namespaced utility."),
            ("How do type hints help in a Python project?", "Type hints document expected values and enable static analyzers and editor tooling to catch some mistakes. Python does not generally enforce them at runtime, so input validation may still be necessary."),
        ],
        "advanced": [
            ("How does Python's method resolution order work with multiple inheritance?", "Python uses the C3 linearization algorithm to produce a consistent method resolution order. Cooperative classes should use `super()` so each implementation in the MRO can participate once."),
            ("What is a descriptor, and where might one be useful?", "A descriptor implements methods such as `__get__`, `__set__`, or `__delete__` to control attribute access. Properties, methods, and many ORM fields use descriptor behavior."),
            ("How should cancellation be handled in an asyncio task?", "Allow cancellation to propagate after performing required cleanup, typically in `finally` blocks or async context managers. Catch `CancelledError` only when there is a specific recovery or translation policy."),
            ("How would you investigate excessive memory use in a Python service?", "Reproduce the workload, measure allocations with tools such as tracemalloc or a profiler, and distinguish retained references from expected caching. Fix the source of retention and validate memory behavior under representative load."),
            ("When is multiprocessing preferable to threading in Python?", "Multiprocessing can run CPU-bound Python work in parallel across processes and avoid the CPython GIL limit on bytecode execution. It adds process startup, serialization, memory, and coordination costs."),
            ("What causes a race condition in threaded Python code?", "A race occurs when the result depends on the timing of concurrent operations on shared state. The GIL does not make multi-step application logic atomic; locks, queues, or immutability can provide safer coordination."),
            ("How can a library preserve compatibility while evolving its public API?", "Define and document the supported public surface, add compatible behavior before deprecating old interfaces, and test against supported versions. Use a deprecation period and clear release notes before removing an API."),
            ("What is the difference between `__new__` and `__init__`?", "`__new__` creates and returns an instance, while `__init__` initializes an instance that has already been created. `__new__` is important for immutable types or specialized instance creation."),
            ("How would you make a Python package build reproducibly?", "Pin or constrain build dependencies, use a standard isolated build configuration, include only intended package files, and build from a clean environment. Verify artifacts and test installation rather than relying on a developer's working tree."),
        ],
    },
    "sql": {
        "basic": [
            ("How does SQL handle NULL in comparisons?", "NULL represents an unknown or missing value, so comparisons such as `column = NULL` do not evaluate true. Use `IS NULL` or `IS NOT NULL`, and account for three-valued logic in filters."),
            ("What does DISTINCT do in a SELECT query?", "DISTINCT removes duplicate result rows based on the selected expressions. It can require extra sorting or hashing, so use it when uniqueness is part of the desired result rather than to hide an unexpected join."),
            ("What is a foreign key?", "A foreign key constrains values in one table to refer to a key in another table or the same table. It helps maintain referential integrity, subject to the database's configured actions and constraints."),
            ("What is the purpose of ORDER BY?", "ORDER BY sorts the returned rows by one or more expressions, with optional ascending or descending direction. Without ORDER BY, row order is not guaranteed."),
            ("How does LIKE perform pattern matching?", "LIKE compares text to a pattern, commonly using `%` for any sequence and `_` for one character. Case sensitivity and escaping behavior depend on the database and collation."),
            ("What is a CASE expression used for?", "CASE evaluates conditions and returns the result for the first matching branch, with an optional ELSE value. It can create conditional values in SELECT, ORDER BY, and other expressions."),
            ("What is the difference between a UNIQUE constraint and a PRIMARY KEY?", "Both enforce uniqueness, but a table has one primary-key constraint that identifies rows and does not allow NULL key values. A table may have multiple UNIQUE constraints, with NULL behavior depending on the database."),
            ("Why should a query list its required columns instead of using SELECT *?", "Selecting explicit columns makes the result contract clearer and avoids transferring unused data. It also reduces surprises when a table schema changes and can help the optimizer use covering indexes."),
        ],
        "intermediate": [
            ("What is a common table expression (CTE)?", "A CTE is a named query expression introduced with WITH and scoped to a statement. It can improve readability and may support recursion, but its optimization or materialization behavior depends on the database."),
            ("What is a correlated subquery?", "A correlated subquery refers to values from the surrounding query and may be evaluated in relation to each outer row. Some optimizers transform it into a join, but performance should be checked with the execution plan."),
            ("How can you find duplicate email addresses in a users table?", "Group by the email column, use `COUNT(*)`, and filter groups with `HAVING COUNT(*) > 1`. Decide how NULL and case normalization should be handled for the application's definition of a duplicate."),
            ("What is a composite index?", "A composite index stores entries for multiple columns in a defined order. Queries can often use its leading columns effectively, so column order should reflect common predicates and sorting requirements."),
            ("What is database normalization?", "Normalization structures relational data to reduce unwanted duplication and update anomalies. The appropriate design depends on integrity needs and query patterns; denormalization can be a deliberate performance trade-off."),
            ("What does ACID mean for database transactions?", "ACID describes atomicity, consistency, isolation, and durability. Together these properties explain important transaction guarantees, though exact isolation and durability behavior depends on the database configuration."),
            ("What information can an EXPLAIN plan provide?", "An EXPLAIN plan shows how the database intends to access and combine data, such as scans, indexes, joins, and estimated costs. Runtime analysis tools may provide actual row counts and timing for comparison."),
            ("How can an upsert handle a row that may already exist?", "An upsert combines insert behavior with a defined conflict action, such as updating selected columns or doing nothing. Syntax and locking details vary by database, and the conflict key must match the intended uniqueness rule."),
        ],
        "advanced": [
            ("How does MVCC help a database manage concurrent transactions?", "Multi-version concurrency control keeps row versions so readers can often observe a consistent snapshot while writers make changes. Old versions require cleanup, and long-running transactions can delay that cleanup."),
            ("What causes a database deadlock, and how should an application respond?", "A deadlock occurs when transactions hold resources while waiting on one another in a cycle. The database typically aborts a victim; applications should handle the error and retry the whole transaction safely when appropriate."),
            ("What is a phantom read?", "A phantom read occurs when repeating a predicate query within a transaction returns a different set of rows because another transaction inserted or removed matching rows. Isolation levels and database implementations determine whether it is prevented."),
            ("How can a covering index improve a query?", "A covering index contains the columns needed by a query, allowing the database to return results without fetching the corresponding table rows in some plans. Larger indexes increase storage and write costs, so validate the workload benefit."),
            ("How does partition pruning improve query performance?", "Partition pruning skips partitions whose key ranges cannot match a query predicate. It works best when predicates align with the partition key and are expressed in a form the optimizer can evaluate."),
            ("Why can a query plan change after statistics are updated?", "The optimizer uses statistics to estimate row counts and selectivity. New statistics can reveal different data distributions and make a different join order or access path appear cheaper; compare estimates with actual execution."),
            ("How would you perform a large schema migration with minimal downtime?", "Use an expand-and-contract rollout: add backward-compatible schema, deploy code that supports both forms, backfill in bounded batches, switch reads and writes, then remove obsolete schema after verification. Monitor locks, lag, and application errors throughout."),
            ("When is a recursive CTE useful, and what safeguards should it have?", "A recursive CTE can traverse hierarchical or graph-like relationships using an anchor query and repeated step. Ensure the recursion has a termination condition, appropriate indexes, and database-specific limits to avoid runaway work."),
            ("How do read replicas affect consistency in an application?", "Replicas can scale reads but may lag behind the primary, so a recently committed write might not be visible immediately. Applications can route consistency-sensitive reads to the primary or use a defined read-after-write strategy."),
        ],
    },
}

for topic_id, levels in PYTHON_SQL_QUESTIONS.items():
    for level, questions in levels.items():
        INTERVIEW_QUESTIONS[topic_id]["questions"][level].extend(questions)

EXTRA_PYTHON_SQL_QUESTIONS = {
    "python": {
        "basic": [
            ("Write a Python program to count how many times each word appears in a sentence.", "Example program:\n\n```python\nsentence = \"learn Python and practice Python\"\nword_counts = {}\n\nfor word in sentence.lower().split():\n    word_counts[word] = word_counts.get(word, 0) + 1\n\nprint(word_counts)\n# {'learn': 1, 'python': 2, 'and': 1, 'practice': 1}\n```\n\nThe dictionary stores each word's running count. `get(word, 0)` supplies zero for a word seen for the first time."),
            ("How can you swap two variable values in Python?", "Use tuple assignment: `first, second = second, first`. Python evaluates the values on the right before assigning them to the names on the left."),
            ("What does `str.strip()` return?", "`strip()` returns a new string with leading and trailing whitespace removed. It does not modify the original string, and it can optionally remove specified characters."),
            ("How do you safely convert text input to an integer?", "Call `int(value)` and handle `ValueError` if the text is not a valid integer. Validate any application-specific range separately after conversion."),
        ],
        "intermediate": [
            ("What is the difference between `map()` and a generator expression?", "`map(function, iterable)` lazily applies a function to each item. A generator expression can express the same transformation inline and is often easier to read when the operation is simple."),
            ("How can you group a list of dictionaries by a field using the standard library?", "Use `collections.defaultdict(list)` and append each record under its field value. For example, loop through records and add each one to `groups[record[\"team\"]]`."),
            ("What does `functools.lru_cache` do, and what should you consider before using it?", "It memoizes function results using argument values as keys, which can avoid repeated work for suitable pure functions. Consider cache size, hashable arguments, stale results, and whether cached values retain too much memory."),
            ("Why is it important to avoid blocking calls inside an asyncio event loop?", "A blocking call prevents the event loop from scheduling other tasks until it returns. Use an asynchronous library or move unavoidable blocking work to an executor."),
        ],
        "advanced": [
            ("How do weak references help prevent certain memory retention problems?", "A weak reference points to an object without increasing its reference count, so it does not keep the object alive by itself. Weak mappings can be useful for caches associated with object lifetimes, but require careful handling when an object has been collected."),
            ("What is the difference between `asyncio.gather()` and `asyncio.TaskGroup`?", "`gather()` awaits multiple awaitables and returns results in input order. `TaskGroup` provides structured concurrency: child tasks are scoped to a block and failures trigger coordinated cancellation and exception reporting."),
            ("How would you design a thread-safe in-memory cache?", "Protect shared mutations with a lock or use a well-defined concurrent abstraction, and define expiration, capacity, and duplicate-work behavior. Keep critical sections short and test concurrent reads, writes, and evictions."),
            ("What does it mean for a Python function to be referentially transparent?", "A referentially transparent function returns the same result for the same inputs and has no observable side effects. This makes reasoning, testing, memoization, and parallel execution easier."),
        ],
    },
    "sql": {
        "basic": [
            ("Write a query to return the three most recently created orders.", "Example query:\n\n```sql\nSELECT order_id, customer_id, created_at\nFROM orders\nORDER BY created_at DESC, order_id DESC\nLIMIT 3;\n```\n\nThe second sort key makes the ordering deterministic when timestamps tie. Some databases use `FETCH FIRST 3 ROWS ONLY` instead of `LIMIT`."),
            ("How do you return rows whose status is either 'Applied' or 'Interview'?", "Use `WHERE status IN ('Applied', 'Interview')`. This is a concise equivalent to combining equality checks with OR."),
            ("What is the difference between an empty string and NULL?", "An empty string is a present text value with zero characters. NULL represents an unknown or missing value and must be checked with `IS NULL`, not ordinary equality."),
            ("How can you give a column a readable name in a query result?", "Use a column alias, such as `SELECT applied_date AS submission_date FROM applications`. An alias changes the result label, not the stored column name."),
        ],
        "intermediate": [
            ("Write a query to count orders for each customer, including customers with no orders.", "Example query:\n\n```sql\nSELECT c.customer_id, COUNT(o.order_id) AS order_count\nFROM customers AS c\nLEFT JOIN orders AS o ON o.customer_id = c.customer_id\nGROUP BY c.customer_id;\n```\n\nUse `COUNT(o.order_id)` rather than `COUNT(*)` so a customer with no matching order gets a count of zero."),
            ("How would you remove duplicate rows while keeping the newest row for each email?", "Use `ROW_NUMBER()` partitioned by a normalized email and ordered by creation time descending, then delete or select rows where the row number is greater than one. First define tie-breaking and NULL behavior, and preview affected rows before deleting."),
            ("What is the difference between UNION and UNION ALL?", "`UNION` combines results and removes duplicate rows, which may require extra work. `UNION ALL` retains duplicates and is generally preferable when deduplication is not required."),
            ("Why can a predicate in the WHERE clause change the results of a LEFT JOIN?", "Filtering a right-side column in WHERE can discard rows where the join produced NULL, making the result behave like an inner join for that condition. Put right-side match conditions in ON when unmatched left rows should remain."),
        ],
        "advanced": [
            ("How would you prevent a lost update when two transactions modify the same account balance?", "Use an atomic update such as `UPDATE accounts SET balance = balance + :delta WHERE account_id = :id`, or read and update within a transaction using an appropriate lock or version check. Verify the affected row count and retry serialization conflicts safely."),
            ("What is a covering index, and when might it be harmful?", "A covering index contains all columns needed for a query so the engine may answer it without reading the base table. It can speed reads but uses storage and increases the cost of inserts, updates, and maintenance."),
            ("How can you make a multi-column keyset-pagination cursor deterministic?", "Order by a unique combination such as `(created_at, id)` and include both last-seen values in the cursor predicate. The predicate should match the sort direction and handle NULL ordering consistently."),
            ("How would you investigate lock contention in a busy database?", "Inspect active transactions, lock waits, deadlock reports, and query plans, then identify long transactions or hot rows. Reduce transaction duration, align indexes with updates, and use a consistent lock order where possible."),
        ],
    },
}

for topic_id, levels in EXTRA_PYTHON_SQL_QUESTIONS.items():
    for level, questions in levels.items():
        INTERVIEW_QUESTIONS[topic_id]["questions"][level].extend(questions)

LEVELS = ("basic", "intermediate", "advanced")


def get_interview_questions(topic: str, level: str):
    if topic not in INTERVIEW_QUESTIONS:
        raise ValueError("Choose a valid interview topic")
    if level not in LEVELS:
        raise ValueError("Choose a valid difficulty level")

    topic_data = INTERVIEW_QUESTIONS[topic]
    return [
        {
            "topic": topic,
            "topic_name": topic_data["name"],
            "level": level,
            "question": question,
            "answer": answer,
        }
        for question, answer in topic_data["questions"][level]
    ]
