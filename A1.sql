-- If you define any views for a question (you are encouraged to), you must drop them
-- after you have populated the answer table for that question.
-- Good Luck!

-- Query 1b i --------------------------------------------------
CREATE VIEW PPE_Testing_Products AS
SELECT sname
FROM ProductTag
INNER JOIN Catalog ON ProductTag.pid = Catalog.pid
INNER JOIN Suppliers ON Catalog.sid = Suppliers.sid
WHERE tagname = 'PPE' OR tagname = 'Testing';

INSERT INTO Query1bi (
    SELECT sname
    FROM PPE_Testing_Products
);

DROP VIEW PPE_Testing_Products;


-- Query 1b ii --------------------------------------------------
CREATE VIEW PPE_Cost_Range AS
SELECT sid
FROM ProductTag
INNER JOIN Catalog ON ProductTag.pid = Catalog.pid
INNER JOIN Suppliers ON Catalog.sid = Suppliers.sid
WHERE tagname = 'PPE' AND (cost < 10 OR cost > 420);

INSERT INTO Query1bii (
    SELECT sid
    FROM PPE_Cost_Range
);

DROP VIEW PPE_Cost_Range;


-- Query 1b iii --------------------------------------------------
CREATE VIEW PPE_Cost_Between_10_1337 AS
SELECT sid
FROM ProductTag
INNER JOIN Catalog ON ProductTag.pid = Catalog.pid
INNER JOIN Suppliers ON Catalog.sid = Suppliers.sid
WHERE tagname = 'PPE' AND (cost >= 10 AND cost <= 1337);

INSERT INTO Query1biii (
    SELECT sid
    FROM PPE_Cost_Between_10_1337
);

DROP VIEW PPE_Cost_Between_10_1337;


-- Query 1b iv  --------------------------------------------------
CREATE VIEW Cleaning_Products AS
SELECT sid
FROM ProductTag
INNER JOIN Catalog ON ProductTag.pid = Catalog.pid
INNER JOIN Suppliers ON Catalog.sid = Suppliers.sid
WHERE tagname = 'Cleaning';

INSERT INTO Query1biv (
    SELECT sid
    FROM Cleaning_Products
);

DROP VIEW Cleaning_Products;


-- Query 1b v --------------------------------------------------
CREATE VIEW Room_Cost_Comparison AS
WITH Catalog1 AS (SELECT * FROM Catalog),
     Catalog2 AS (SELECT * FROM Catalog)
SELECT c1.sid, c2.sid
FROM Catalog1 c1
JOIN Catalog2 c2 ON c1.cost >= 1.2 * c2.cost;

INSERT INTO Query1bv (
    SELECT *
    FROM Room_Cost_Comparison
);

DROP VIEW Room_Cost_Comparison;


-- Query 1b vi --------------------------------------------------
CREATE VIEW Common_Products AS
WITH Catalog1 AS (SELECT * FROM Catalog),
     Catalog2 AS (SELECT * FROM Catalog)
SELECT DISTINCT c1.pid
FROM Catalog1 c1
CROSS JOIN Catalog2 c2
WHERE c1.sid <> c2.sid;

INSERT INTO Query1bvi (
    SELECT *
    FROM Common_Products
);

DROP VIEW Common_Products;


-- Query 1b vii --------------------------------------------------
CREATE VIEW Unique_Suppliers AS
WITH SuperTechProducts AS (
SELECT sid, cost
FROM ProductTag
INNER JOIN Catalog ON ProductTag.pid = Catalog.pid
INNER JOIN Suppliers ON Catalog.sid = Suppliers.sid
WHERE tagname = 'Super Tech' AND scountry = 'USA'
),
MaxCost AS (
SELECT MAX(cost) AS max_cost
FROM SuperTechProducts
),
MatchingSuppliers AS (
SELECT sid, cost
FROM SuperTechProducts
CROSS JOIN MaxCost
WHERE cost < max_cost
),
UniqueSuppliers AS (
SELECT sid, cost
FROM SuperTechProducts
EXCEPT
SELECT sid, cost
FROM MatchingSuppliers
)
SELECT DISTINCT sid
FROM UniqueSuppliers;

INSERT INTO Query1bvii (
    SELECT *
    FROM Unique_Suppliers
);

DROP VIEW Unique_Suppliers;

-- Query 1b ix --------------------------------------------------
CREATE VIEW High_Cost_Products AS
SELECT pid
FROM Catalog
WHERE cost >= 69;

INSERT INTO Query1bix (
    SELECT pid
    FROM Product
    EXCEPT
    SELECT pid
    FROM High_Cost_Products
);

DROP VIEW High_Cost_Products;


-- Query 1b x --------------------------------------------------
CREATE VIEW Product_In_Inventory AS
SELECT pid
FROM Inventory;

INSERT INTO Query1bx (
    SELECT pid
    FROM Product
    EXCEPT
    SELECT pid
    FROM Product_In_Inventory
);

DROP VIEW Product_In_Inventory;


-- Query 1c i --------------------------------------------------
CREATE VIEW CommonProducts1 AS
SELECT sid, subid, pid, cost
FROM Subsuppliers AS s1
JOIN Subsuppliers AS s2 ON s1.pid = s2.pid;

CREATE VIEW CommonProducts2 AS
SELECT sid, subid, pid, cost
FROM Subsuppliers AS s1
JOIN Subsuppliers AS s2 ON s1.pid = s2.pid;

CREATE VIEW CommonProducts AS
SELECT cp1.pid, cp1.sid AS sid1, cp2.sid AS sid2, cp1.cost AS cost1, cp2.cost AS cost2
FROM CommonProducts1 AS cp1
JOIN CommonProducts2 AS cp2 ON cp1.pid = cp2.pid
WHERE cp1.sid != cp2.sid AND cp1.cost = cp2.cost;

INSERT INTO Query1ci (
    SELECT DISTINCT pid, sid1, sid2, cost1, cost2
    FROM CommonProducts
);

DROP VIEW CommonProducts1;
DROP VIEW CommonProducts2;
DROP VIEW CommonProducts;




-- Query 1c ii --------------------------------------------------
CREATE VIEW ProductPairs AS
SELECT c1.pid, c1.sid, c1.cost
FROM Catalog AS c1
JOIN Catalog AS c2 ON c1.pid = c2.pid;

CREATE VIEW UniqueProductPairs AS
SELECT DISTINCT pid1, cost1
FROM ProductPairs;

CREATE VIEW UniquePrices AS
SELECT pp.pid, pp.sid, pp.cost
FROM ProductPairs AS pp
JOIN UniqueProductPairs AS upp ON pp.pid = upp.pid1 AND pp.cost = upp.cost1;

INSERT INTO Query1cii (
    SELECT DISTINCT pid, sid, cost
    FROM UniquePrices
);

DROP VIEW ProductPairs;
DROP VIEW UniqueProductPairs;
DROP VIEW UniquePrices;



-- Query 1c iii --------------------------------------------------
CREATE VIEW PPEProducts AS
SELECT pid
FROM ProductTag
WHERE tagname = 'PPE';

CREATE VIEW NonSuperTechProducts AS
SELECT pid
FROM ProductTag
WHERE tagname != 'Super Tech';

CREATE VIEW OtherProducts AS
SELECT pid
FROM ProductTag
WHERE tagname != 'Super Tech' AND tagname != 'PPE';

CREATE VIEW CommonProducts AS
SELECT pid
FROM PPEProducts
INTERSECT
SELECT pid
FROM NonSuperTechProducts
INTERSECT
SELECT pid
FROM OtherProducts;

INSERT INTO Query1ciii (
    SELECT p.pid, p.pname, c.cost
    FROM CommonProducts AS cp
    JOIN Product AS p ON cp.pid = p.pid
    JOIN Catalog AS c ON p.pid = c.pid
);

DROP VIEW PPEProducts;
DROP VIEW NonSuperTechProducts;
DROP VIEW OtherProducts;
DROP VIEW CommonProducts;


-- Query 1c iv  --------------------------------------------------
CREATE VIEW Subsuppliers1 AS
SELECT * FROM Subsuppliers;

CREATE VIEW Subsuppliers2 AS
SELECT * FROM Subsuppliers;

CREATE VIEW SuppliersWithBusinessRelationship AS
SELECT sid, subid, sname, saddress
FROM (
    SELECT s1.sid, s1.subid, s1.sname, s1.saddress
    FROM Subsuppliers1 s1
    JOIN Subsuppliers2 s2 ON s1.sid = s2.subid AND s1.subid = s2.sid
    UNION ALL
    SELECT s2.sid, s2.subid, s2.sname, s2.saddress
    FROM Subsuppliers1 s1
    JOIN Subsuppliers2 s2 ON s1.sid = s2.subid AND s1.subid = s2.sid
) AS SuppliersWithBusinessRelationship;

CREATE VIEW ReversedSuppliersWithBusinessRelationship AS
SELECT subid, sid, sname, saddress
FROM (
    SELECT s1.sid, s1.subid, s1.sname, s1.saddress
    FROM Subsuppliers1 s1
    JOIN Subsuppliers2 s2 ON s1.sid = s2.subid AND s1.subid = s2.sid
    UNION ALL
    SELECT s2.sid, s2.subid, s2.sname, s2.saddress
    FROM Subsuppliers1 s1
    JOIN Subsuppliers2 s2 ON s1.sid = s2.subid AND s1.subid = s2.sid
) AS ReversedSuppliersWithBusinessRelationship;

INSERT INTO Query1civ (
    SELECT sid, subid, sname, saddress
    FROM SuppliersWithBusinessRelationship
    EXCEPT
    SELECT subid, sid, sname, saddress
    FROM ReversedSuppliersWithBusinessRelationship
);

DROP VIEW Subsuppliers1;
DROP VIEW Subsuppliers2;
DROP VIEW SuppliersWithBusinessRelationship;
DROP VIEW ReversedSuppliersWithBusinessRelationship;


-- Query 2 i --------------------------------------------------
CREATE VIEW Room404Students AS
SELECT s.utorid
FROM Student s
LEFT JOIN Approved a ON s.utorid = a.utorid
LEFT JOIN Room r ON a.roomid = r.roomid
WHERE r.roomname = 'IC404' AND a.utorid IS NULL;

INSERT INTO Query2bi (
    SELECT utorid
    FROM Room404Students
);

DROP VIEW Room404Students;



-- Query 2 ii --------------------------------------------------
CREATE VIEW EmployeeRoomCounts AS
WITH EmployeeRooms AS (
    SELECT e.utorid, a.roomid
    FROM Employee e
    JOIN Approved a ON e.utorid = a.utorid
)
SELECT er.utorid, COUNT(er.roomid) AS room_count
FROM EmployeeRooms er
GROUP BY er.utorid;

INSERT INTO Query2bii (
    SELECT utorid
    FROM EmployeeRoomCounts
    WHERE room_count >= 3
);

DROP VIEW EmployeeRoomCounts;



-- Query 2 iii --------------------------------------------------
CREATE VIEW EmployeeRoomCounts AS
WITH EmployeeRooms AS (
    SELECT e.utorid, a.roomid
    FROM Employee e
    JOIN Approved a ON e.utorid = a.utorid
)
SELECT er.utorid, COUNT(er.roomid) AS room_count
FROM EmployeeRooms er
GROUP BY er.utorid;

INSERT INTO Query2biii (
    SELECT utorid
    FROM EmployeeRoomCounts
    WHERE room_count = 3
);

DROP VIEW EmployeeRoomCounts;


-- Query 2 iv  --------------------------------------------------
CREATE VIEW EmployeeRoomCounts AS
WITH EmployeeRooms AS (
    SELECT e.utorid, a.roomid
    FROM Employee e
    JOIN Approved a ON e.utorid = a.utorid
)
SELECT er.utorid, COUNT(er.roomid) AS room_count
FROM EmployeeRooms er
GROUP BY er.utorid;

INSERT INTO Query2biv (
    SELECT utorid
    FROM EmployeeRoomCounts
    WHERE room_count <= 3
);

DROP VIEW EmployeeRoomCounts;



-- Query 2 v --------------------------------------------------
CREATE VIEW ExceededThresholdRooms AS
SELECT DISTINCT o.roomid
FROM Member m
JOIN Approved a ON m.utorid = a.utorid
JOIN Room r ON a.roomid = r.roomid
JOIN Occupancy o ON m.utorid = o.utorid AND r.roomid = o.roomid
WHERE m.name = 'Oscar Lin' AND o.date >= '2022-09-01' AND o.date <= '2022-12-31' AND o.alertlevel > r.alertthreshold;

INSERT INTO Query2bv (
    SELECT *
    FROM ExceededThresholdRooms
);

DROP VIEW ExceededThresholdRooms;


-- Query 2 vi --------------------------------------------------
CREATE VIEW UnapprovedTravelers AS
SELECT DISTINCT m.utorid
FROM Member m
LEFT JOIN Approved a ON m.utorid = a.utorid
LEFT JOIN Room r ON a.roomid = r.roomid
LEFT JOIN Occupancy o ON m.utorid = o.utorid AND r.roomid = o.roomid
WHERE o.date >= '2021-03-17' AND o.date <= '2022-12-31' AND a.utorid IS NULL;

INSERT INTO Query2bvi (
    SELECT *
    FROM UnapprovedTravelers
);

DROP VIEW UnapprovedTravelers;


-- Query 2 viii --------------------------------------------------
CREATE VIEW UnvaccinatedExceededThreshold AS
SELECT DISTINCT m.utorid, m.email
FROM Member m
JOIN Occupancy o ON m.utorid = o.utorid
JOIN Room r ON o.roomid = r.roomid
JOIN Approved a ON m.utorid = a.utorid AND o.roomid = a.roomid
WHERE m.vaxstatus = 0 AND o.alertlevel > r.alertthreshold;

INSERT INTO Query2bviii (
    SELECT *
    FROM UnvaccinatedExceededThreshold
);

DROP VIEW UnvaccinatedExceededThreshold;












