package it.sistinf.romacapitale.management.repository;

import it.sistinf.romacapitale.core.persistence.sql.AbstractRepository;
import it.sistinf.romacapitale.management.entity.AmbitoEntity;
import org.springframework.stereotype.Repository;

@Repository
public class AmbitoRepository extends AbstractRepository<String, AmbitoEntity> {

    public AmbitoRepository() {
        super(AmbitoEntity.class);
    }
}
