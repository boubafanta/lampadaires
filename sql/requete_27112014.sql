SELECT * FROM quartier

--Liste des lampadaires d'un état X d'un quartier Y
create or replace function etat_quartier(etat text, quartier integer)
  returns table (param_id integer, param_states text, param_geom geometry)
as
$body$
	SELECT l.gid,l.states,l.geom
	FROM quartier AS q
	JOIN lampadaire AS l
	ON st_dwithin(l.geom,q.geom,0)
	WHERE l.states = $1 
	AND q.gid = $2
$body$
language sql;

-- Test : SELECT * FROM etat_quartier('ok',2)

--============== Afficher l'itinéraire d'un point A à un point B en passant par le chemin le plus court éclairé à X% ===============

-- Step 1 = on crée la vue des troncons eclaires
CREATE OR REPLACE VIEW public.tronconec AS 
 SELECT t.gid,
    t.nam,
    t.id_start,
    t.id_end,
    t.typ,
    t.v_moy,
    COALESCE(te.coeff_eclairage, 0::double precision) AS coeff_eclairage,
    t.geom
   FROM troncon t
     LEFT JOIN troncon_eclairage te ON t.gid = te.id_troncon;

-- Step 2 = on crée la fonction associée avec les paramètres en entrée A, B et X

create or replace function itineraire(A integer, B integer, C float)
  returns table (param_seq integer, param_node integer, param_edge integer, param_cost float, param_coef float, param_geom geometry)
as
$body$
	SELECT seq, id1 as node, id2 as edge,  cost , coeff_eclairage, geom FROM pgr_dijkstra('
		SELECT gid AS id,
			id_start::integer as source,
			id_end::integer as target,
			st_length(geom) as cost,
			coeff_eclairage
			FROM tronconec where coeff_eclairage>'||$3,
		$1,$2,false,false)
join tronconec as tr
on id2 = tr.gid
$body$
language sql;

-- Step 3 = Récupérer l'id du point le plus proche des coordonnées (X,Y)
create or replace function pointD(X float, Y float)
  returns integer
as	
$body$
	SELECT gid 
	FROM tronconec AS t
	ORDER BY t.geom <-> ST_transform(ST_setsrid(ST_MakePoint($1,$2),4326),32628)
	LIMIT 1
$body$ 
language sql;

-- Step 4 = Récupérer le tronçon
create or replace function iti(X1 float, Y1 float,X2 float, Y2 float, C float)
  returns table (param_seq integer, param_node integer, param_edge integer, param_cost float, param_coef float, param_geom geometry)
as
$body$
	--with n1 as (SELECT * FROM point($1,$2)), n2 as (SELECT * FROM point($3,$4))
	SELECT * FROM itineraire(pointD($1,$2),pointD($3,$4),$5)
$body$
language sql;


-- Test 
--SELECT *
--FROM itineraire(1366,2348,50)

